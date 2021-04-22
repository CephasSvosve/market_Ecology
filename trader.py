from marketMaker import marketMaker
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

        self.numberofshares    = pd.DataFrame(columns= self.marketMaker.stockPrice.columns)   
        self.balanceSheet      = [initialWealth]                             
        self.cashAccount       = [0]
        self.cashFlow          = [500]
        self.excessDemand      = pd.DataFrame(columns= self.marketMaker.stockPrice.columns)
           
        





        self.stockValue        = pd.DataFrame(columns= self.marketMaker.stockPrice.columns) 
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
        cashFlow_t = 0





        #Where W_i_t is the wealth invested in asset i at time t
        #W_t is the total wealth at time t comprising of the sum of wealth invested in all individual assets plus 
        # wealth in bonds plus interest on bonds and new wealth introduced at time t


    

        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]
        W_t        = np.sum(W_i_t) +  self.cashAccount[-1] * (1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     




        self.cashFlow.append(cashFlow_t)




        #Using the value, we then calculate the trading signal for each stock in the dataframe 
        marketCapital_i = [self.stockPrice[tickerID].values[tau] * self.marketMaker.stockInventory[tickerID].values[tau]for tickerID in  self.numberofshares.columns]
        
        
        signalVT_i      = [tickerID/np.sum(marketCapital_i) for tickerID in marketCapital_i]
        

        
        
        

        demand_i     = []
        for x,tickerID in enumerate(self.numberofshares.columns):
            if (t==tau):
                #given we only invest in the stock that shows the maximum signal
                if (marketCapital_i[x] >= np.sort(marketCapital_i)[1]):
                    d  =  self.leverage * W_t * signalVT_i[x]/self.stockPrice[tickerID].values[t]
                else:
                    d = 0
            else:
                if (marketCapital_i[x]  >= np.sort(marketCapital_i)[1]):
                    d  =  self.leverage * self.cashFlow[t]  * signalVT_i[x]/self.stockPrice[tickerID].values[t]
                else:
                    d = 0

            demand_i.append(d)



        



        investedWealth   = np.array(demand_i )* np.array(self.stockPrice.iloc[-1])
        uninvestedWealth = W_t - np.sum(investedWealth)
        



        self.numberofshares.loc[len(self.numberofshares)]  =  demand_i 
        self.excessDemand.loc[len(self.excessDemand)]      =  self.numberofshares.iloc[-1] - self.numberofshares.iloc[-2]
        self.stockValue.loc[len(self.stockValue)]          =  np.sign(self.stockPrice.iloc[-1])*self.stockPrice.iloc[-1]**2
        self.cashAccount.append(uninvestedWealth)
        self.balanceSheet.append(W_t)

        

        return   np.array(demand_i)








    def valueTrader(self):    



        t          = self.marketWatch
        tau        = np.int(self.rebalancingPeriod * np.floor(t/self.rebalancingPeriod))
        cashFlow_t = 0





        #Where W_i_t is the wealth invested in asset i at time t
        #W_t is the total wealth at time t comprising of the sum of wealth invested in all individual assets plus 
        # wealth in bonds plus interest on bonds and new wealth introduced at time t


       

        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]
        W_t        = np.sum(W_i_t) +  self.cashAccount[-1] * (1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     




        self.cashFlow.append(cashFlow_t)




        #We calculate value of each stock using the trader's method of valuing the stocks and update the  stockValue dataframe
        self.stockValue.loc[len(self.stockValue)] = [5*self.stockValue[tickerID].values[-1] for tickerID in self.stockValue.columns ]





        #Using the value, we then calculate the trading signal for each stock in the dataframe 
        signalVT_i   = [np.log2(self.stockValue[tickerID].values[tau])-np.log2(self.stockPrice[tickerID].values[tau]) for tickerID in  self.stockValue.columns]
        


        


        demand_i     = []
        for x,tickerID in enumerate(self.numberofshares.columns):
            if (t==tau):
                #given we only invest in the stock that shows the maximum signal
                if np.abs(signalVT_i[x]) == max(np.abs(signalVT_i)):
                    d  =  np.sign(signalVT_i[x]) * self.leverage * W_t * (np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                else:
                    d = 0
            else:
                if np.abs(signalVT_i[x]) == max(np.abs(signalVT_i)):
                    d  =  np.sign(signalVT_i[x]) * self.leverage * self.cashFlow[-1]  * (np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                else:
                    d = 0

            demand_i.append(d)

        





        investedWealth   = np.array(demand_i )* np.array(self.stockPrice.iloc[-1])
        uninvestedWealth = W_t - np.sum(investedWealth)
        



        self.numberofshares.loc[len(self.numberofshares)]  =  demand_i 
        self.excessDemand.loc[len(self.excessDemand)]      =  self.numberofshares.iloc[-1] - self.numberofshares.iloc[-2]
        self.stockValue.loc[len(self.stockValue)]          =  np.sign(self.stockPrice.iloc[-1])*self.stockPrice.iloc[-1]**2
        self.cashAccount.append(uninvestedWealth)
        self.balanceSheet.append(W_t)

        

        return   np.array(demand_i)







    def trendFollower(self):
        
        t          = self.marketWatch
        tau        = np.int(self.rebalancingPeriod * np.floor(t/self.rebalancingPeriod))
        cashFlow_t = 0
        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]
        W_t        = np.sum(W_i_t) +  self.cashAccount[-1] * (1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     

        




        self.cashFlow.append(cashFlow_t)

 





        signalVT_i   = []
        for tickerID in  self.stockValue.columns:
            if(len(self.stockPrice[tickerID].values) < self.rebalancingPeriod):
                 a =np.log2(self.stockPrice[tickerID].values[tau])-np.log2(self.stockPrice[tickerID].values[tau])
            else:
                 a =np.log2(self.stockPrice[tickerID].values[tau])-np.log2(self.stockPrice[tickerID].values[tau-self.rebalancingPeriod])
            
            signalVT_i.append(a)








        demand_i     = []
        for x,tickerID in enumerate(self.numberofshares.columns):
            if (t==tau):
                #given we only invest in the stock that shows the maximum signal
                if np.abs(signalVT_i[x]) == max(np.abs(signalVT_i)):
                    d  =  np.sign(signalVT_i[x]) * self.leverage * W_t * (np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                else:
                    d = 0
            else:
                if np.abs(signalVT_i[x]) == max(np.abs(signalVT_i)):
                    d  =  np.sign(signalVT_i[x]) * self.leverage * self.cashFlow[-1]  * (np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                else:
                    d = 0

            demand_i.append(d)









        investedWealth   = np.array(demand_i )* np.array(self.stockPrice.iloc[-1])
        uninvestedWealth = W_t - np.sum(investedWealth)
        



        self.numberofshares.loc[len(self.numberofshares)]  =  demand_i 
        self.excessDemand.loc[len(self.excessDemand)]      =  self.numberofshares.iloc[-1] - self.numberofshares.iloc[-2]
        self.stockValue.loc[len(self.stockValue)]          =  np.sign(self.stockPrice.iloc[-1])*self.stockPrice.iloc[-1]**2
        self.cashAccount.append(uninvestedWealth)
        self.balanceSheet.append(W_t)

        

        return  np.array(demand_i)
      








    def noiseTrader(self):    

        t          = self.marketWatch
        tau        = np.int(self.rebalancingPeriod * np.floor(t/self.rebalancingPeriod))
        cashFlow_t = 0
        W_i_t      = [self.numberofshares[tickerID].values[-1] * self.stockPrice[tickerID].values[-1]  for tickerID in  self.stockPrice.columns]
        W_t        = np.sum(W_i_t) +  self.cashAccount[-1] * (1+ self.marketMaker.riskFreeRate) + self.cashFlow[-1]     

        #W_i_t is the wealth invested in asset i at time t
            #W_t is the total wealth at time t comprising of the sum of wealth invested in all individual assets plus 
                # wealth in bonds plus interest on bonds and new wealth introduced at time t






        self.cashFlow.append(cashFlow_t)





        #We calculate value of each stock using the trader's method of valuing the stocks and update the  stockValue dataframe
        self.stockValue.loc[len(self.stockValue)] = [5*self.stockValue[tickerID].values[-1] for tickerID in self.stockValue.columns ]

        dX = rho*(mu - X)*dt + sd*dW








        #Using the value, we then calculate the trading signal for each stock in the dataframe 
        signalVT_i   = [np.log2(self.stockValue[tickerID].values[tau])-np.log2(self.stockPrice[tickerID].values[tau]) for tickerID in  self.stockValue.columns]
        









        demand_i     = []
        for x,tickerID in enumerate(self.numberofshares.columns):
            if (t==tau):
                #given we only invest in the stock that shows the maximum signal
                if np.abs(signalVT_i[x]) == max(np.abs(signalVT_i)):
                    d  =  np.sign(signalVT_i[x]) * self.leverage * W_t * (np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                else:
                    d = 0
            else:
                if np.abs(signalVT_i[x]) == max(np.abs(signalVT_i)):
                    d  =  np.sign(signalVT_i[x]) * self.leverage * self.cashFlow[-1]  * (np.tanh(signalVT_i[x]+np.log(2)))/self.stockPrice[tickerID].values[t] 
                else:
                    d = 0

            demand_i.append(d)









        investedWealth   = np.array(demand_i )* np.array(self.stockPrice.iloc[-1])
        uninvestedWealth = W_t - np.sum(investedWealth)
        



        self.numberofshares.loc[len(self.numberofshares)]  =  demand_i 
        self.excessDemand.loc[len(self.excessDemand)]      =  self.numberofshares.iloc[-1] - self.numberofshares.iloc[-2]
        self.stockValue.loc[len(self.stockValue)]          =  np.sign(self.stockPrice.iloc[-1])*self.stockPrice.iloc[-1]**2
        
        self.cashAccount.append(uninvestedWealth)
        self.balanceSheet.append(W_t)

        

        return   np.array(demand_i)




                                              
        
     



#Trader's communication point with the market maker

    def receiveQoutes(self, stockPriceDF, marketWatch):   
        self.stockPrice  =  stockPriceDF                                           
        self.marketWatch =  marketWatch

    def sendOrder(self):
        print()
   








#Trader's action point

    def respond(self):   
                                            
            if self.strategy   == 'valueTrader':
                return self.valueTrader()
            elif self.strategy == 'noiseTrader':
                return self.noiseTrader()
            elif self.strategy == 'trendFollower':
                return self.trendFollower()
            elif self.strategy == 'passiveTrader':
                return self.passiveTrader()
       