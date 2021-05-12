from marketMaker import marketMaker
from dataFrameControl import dfControl as df
import numpy as np
import pandas as pd 
import sys



class trader:
    def __init__(self, strategy, rebalancingPeriod, leverage, initialWealth, marketMaker):




#We state the trader's constant attributes

        self.strategy          = strategy                                   
        self.rebalancingPeriod = rebalancingPeriod
        self.leverage          = leverage
        self.marketMaker       = marketMaker






#We state the trader's dynamic attributes

        self.numberofshares    = pd.DataFrame(columns = self.marketMaker.stockPrice.columns)   
        self.balanceSheet      = [initialWealth]                             
        self.cashAccount       = [0]
        self.cashFlow          = [initialWealth]
        self.excessDemand      = pd.DataFrame(columns= self.marketMaker.stockPrice.columns)
           
        


       
        #For the Ornstein Uhlenbeck process used on the noise trader's model, we wish to store the previous random noise term
        # so we create the random variable X that we will use to generate noise in the noise trader's function outside
        #the function so that the stored value is not altered each time we call the function
        self.X   = [np.random.normal(0,1)] 


        self.stockValue        = pd.DataFrame(columns = self.marketMaker.stockPrice.columns) 
        #This is a dataframe of the value of each of the stocks available calculated according to the trader's own formula
            #We assume that all stocks are introduced at the beginning of the whole process so that
                #we can use columns in the marketMaker's stockPrice Dataframe
    





        self.numberofshares.loc[len(self.numberofshares)] = [0 for i in self.numberofshares.columns]
        self.excessDemand.loc[len(self.excessDemand)]     = [0 for i in self.excessDemand.columns]
        self.stockValue.loc[len(self.stockValue)]         = [5 for i in self.stockValue.columns]








#We define the trading strategies

    def passiveTrader(self):                                                
       
        t          = self.marketWatch
        tau        = np.int(self.rebalancingPeriod * np.floor(t/self.rebalancingPeriod))
        



        #Where W_i_t is the wealth invested in asset i at time t
        #W_t is the total wealth at time t comprising of the sum of wealth invested in all individual assets plus 
        # wealth in bonds plus interest on bonds and new wealth introduced at time t


    

        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]


        W_t        = np.sum(
            W_i_t) +  self.cashAccount[-1] * (
                1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     



        cashFlow_t = np.float(np.random.normal(0,200))
        self.cashFlow.append(cashFlow_t)
        




        #Using the value, we then calculate the trading signal for each stock in the dataframe 
        marketCapital_i = [df.getColumn(tickerID,self.stockPrice,False).values[tau] * df.getColumn(tickerID,self.marketMaker.stockInventory,False).values[tau] for tickerID in  self.numberofshares.columns]
        
        
        signal_i      = [tickerID/np.sum(marketCapital_i) for tickerID in marketCapital_i]
        

        
        
        
       



        #n stock world, investor picking one stock with highest signal;
        demand_i = self.computeDemand(signal_i,W_t,cashFlow_t,t,tau)
        self.updateRecords(demand_i,W_t)
        
        

        
       
        return   np.array(demand_i)








    def valueTrader(self):    



        t          = self.marketWatch
        tau        = np.int(self.rebalancingPeriod * np.floor(t/self.rebalancingPeriod))
        





        #Where W_i_t is the wealth invested in asset i at time t
        #W_t is the total wealth at time t comprising of the sum of wealth invested in all individual assets plus 
        # wealth in bonds plus interest on bonds and new wealth introduced at time t


       

        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]




        W_t        = np.sum(
            W_i_t) +  self.cashAccount[-1] * (
                1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     



        cashFlow_t = np.float(np.random.normal(0,200))
        self.cashFlow.append(cashFlow_t)

       
        #We calculate value of each stock using the trader's method of valuing the stocks and update the  stockValue dataframe
        self.stockValue.loc[len(self.stockValue)] = [5*self.stockValue[tickerID].values[-1] for tickerID in self.stockValue.columns ]





        #Using the value, we then calculate the trading signal for each stock in the dataframe 
        signal_i   = [np.log2(
            self.stockValue[tickerID].values[tau])-np.log2(
                self.stockPrice[tickerID].values[tau]) for tickerID in  self.stockValue.columns]
        


        demand_i = self.computeDemand(signal_i,W_t,cashFlow_t,t,tau)
       
        self.updateRecords(demand_i,W_t)

        

        return   np.array(demand_i)







    def trendFollower(self):
        
        t          = self.marketWatch



        tau        = np.int(
            self.rebalancingPeriod * np.floor(
                t/self.rebalancingPeriod))





        #Where W_i_t is the wealth invested in asset i at time t
        #W_t is the total wealth at time t comprising of the sum of wealth invested in all 
        # individual assets plus 
        # wealth in bonds plus interest on bonds and new wealth introduced at time t


        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]



        W_t        = np.sum(
            W_i_t) +  self.cashAccount[-1] * (
                1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     

        


        cashFlow_t = np.float(np.random.normal(0,200))
        self.cashFlow.append(cashFlow_t)

 




        #Because trend follower compares next price to the previous one, we have to set
        #a careful condition to take care of time 0 because a second price has not yet 
        #been generated

        signal_i   = []
        for tickerID in  self.stockValue.columns:
            if(len(self.stockPrice[tickerID].values) < self.rebalancingPeriod):
                 a =np.log2(self.stockPrice[tickerID].values[tau])-np.log2(self.stockPrice[tickerID].values[tau])
            else:
                 a =np.log2(self.stockPrice[tickerID].values[tau])-np.log2(self.stockPrice[tickerID].values[tau-self.rebalancingPeriod])
            
            signal_i.append(a)





        demand_i = self.computeDemand(signal_i,W_t,cashFlow_t,t,tau)
        self.updateRecords(demand_i,W_t)


        return  np.array(demand_i)
      






    def noiseTrader(self):    

        t          = self.marketWatch




        tau        = np.int(
            self.rebalancingPeriod * np.floor(
                t/self.rebalancingPeriod))



        
        







        #W_i_t is the wealth invested in asset i at time t
        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]







        #W_t is the total wealth at time t comprising of the sum of wealth invested in all 
        # individual assets plus 
        # wealth in bonds plus interest on bonds and new wealth introduced at time t


        W_t        = np.sum(
            W_i_t) +  self.cashAccount[-1] * (
                1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]   


        cashFlow_t = np.float(np.random.normal(0,200))
        self.cashFlow.append(cashFlow_t)
        


        #We calculate value of each stock using the trader's method of valuing the stocks and update the  stockValue dataframe
        value = [5*df.getColumn(tickerID,self.stockValue,lastValueOnly=True) for tickerID in self.stockValue.columns]
        df.appendNextRow(self.stockValue,value)



        dt  = self.rebalancingPeriod
        dW  = np.random.normal(0,self.rebalancingPeriod)
        rho = 0.104943177
        mu  = 1
        sd  = 0.12

        

        Xt       = rho*(mu - self.X[-1])*dt + sd*dW
        self.X.append(Xt)




        #Using the value, we then calculate the trading signal for each stock in the dataframe 
        signal_i   = [np.log2(
            np.abs(self.X[-1])*self.stockValue[tickerID].values[tau])-np.log2(
                self.stockPrice[tickerID].values[tau]) for tickerID in  self.stockValue.columns] #correct this line
        


        demand_i = self.computeDemand(signal_i,W_t,cashFlow_t,t,tau)
        self.updateRecords(demand_i,W_t)
        

        return   np.array(demand_i)




                                              
        
     



#Trader's communication point with the market maker

    def receiveQoutes(self, stockPriceDF, marketWatch):   
        self.stockPrice  =  stockPriceDF                                           
        self.marketWatch =  marketWatch

    def sendOrder(self):
        print()


    
    def computeDemand(self,signal_i,W_t,cashFlow,t,tau):
        demand = self.demandMethod(len(signal_i),signal_i,W_t,cashFlow,t,tau)

        return demand
        
        
        

    def demandMethod(self,argument,signal_i,wealth,cashFlow,t,tau):
        demand = []
        if(argument <= 1):
            #Maarten's Algorithm
            demand = [self.leverage * wealth * (np.tanh(signal_i)+0.5)]
           
            
        

        elif(argument == 2): 
            for x,tickerID in enumerate(self.numberofshares.columns):
                if(x<1):
                    d1  =  self.leverage * 0.6 * wealth * (
                            1/df.getColumn(tickerID,self.stockPrice,False).values[tau])*(
                                1/(1 + np.exp(
                                    -(signal_i[0]-signal_i[1])))) + (
                                        self.leverage * 0.6 * cashFlow * (
                                                    1/df.getColumn(
                                                        tickerID,self.stockPrice,False).values[t])*(
                                                            1/(
                                                                1 + np.exp(
                                                                            -(
                                                                                signal_i[0]-signal_i[1])))))



                    d2  =  self.leverage * 0.6 * wealth * (
                        1/df.getColumn(tickerID,self.stockPrice,False).values[tau])*(1-(
                            1/(1 + np.exp(
                                -(signal_i[0]-signal_i[1]))))) + (
                                    self.leverage * 0.6 * cashFlow * (
                                                1/df.getColumn(
                                                    tickerID,self.stockPrice,False).values[t])*(
                                                        1/(
                                                                1 + np.exp(
                                                                        -(
                                                                            signal_i[0]-signal_i[1])))))

                                

                
                
                    

                    demand.append(d1)
                    demand.append(d2)
                
                
                
                

        else:
                print('Code not yet implemented')
                # #n stock world, investor picking one stock with highest signal;
                #demand_i = []
                # for x,tickerID in enumerate(self.numberofshares.columns):
                #     if (t==tau):
                #         #given we only invest in the stock that shows the maximum signal
                #         if np.abs(signalVT_i[x]) == max(
                #             np.abs(signalVT_i)):
                #             d  =  np.sign(
                #                 signalVT_i[x]) * self.leverage * W_t * (
                #                     np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 

                #         else:
                #             d = 0          
                #     else:
                #         if np.abs(
                #             signalVT_i[x]) == max(np.abs(signalVT_i)):
                #             d  =  np.sign(
                #                 signalVT_i[x]) * self.leverage * self.cashFlow[-1]  * (
                #                     np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                #         else:
                #             d = 0

                #     demand_i.append(d)
        
        return demand


        


    def updateRecords(self,demand_i,W_t):
        
        

        investedWealth   = np.array(demand_i) * np.array((self.marketMaker.stockPrice.iloc[-1]))
        unInvestedWealth = W_t - np.sum(investedWealth)
        value            = df.getLastRow(self.stockValue)/0.02
        netDemand        = df.getLastRow(
            self.numberofshares)-df.getPenultimateRow(self.numberofshares)   



        df.appendNextRow(self.numberofshares,demand_i)
        df.appendNextRow(self.excessDemand,netDemand)
        df.appendNextRow(self.stockValue,value )
        self.cashAccount.append(unInvestedWealth)
        self.balanceSheet.append(W_t)

    







#Trader's action point

    def respond(self):   
        #try:                                   
            if self.strategy   == 'valueTrader':
                return self.valueTrader()
            elif self.strategy == 'noiseTrader':
                return self.noiseTrader()
            elif self.strategy == 'trendFollower':
                return self.trendFollower()
            elif self.strategy == 'passiveTrader':
                return self.passiveTrader()
        #except:
           # print(f'Check {self.strategy}')
       