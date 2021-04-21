import numpy as np
import pandas as pd 


class marketMaker:
    def __init__(self):
        self.stockInventory = pd.DataFrame()
        self.stockPrice     = pd.DataFrame()
        self.stockBid       = pd.DataFrame()
        self.stockAsk       = pd.DataFrame()
        self.stockSpread    = pd.DataFrame()
        self.balanceSheet   = []
        self.riskFreeRate   = 0
        self.submittedDemand= []
        






    #This is a method that we use to introduce securities into the market
    def IPO(self, tickerID, initialPrice, outstandingShares):






        #We add the newstock to the stockInventory dataframe and update other dataframes accordingly
        #We set all dataframe entries prior to the IPO to zero to avoid missing entry errors

        self.stockInventory[tickerID]  = [outstandingShares]
        self.stockPrice[tickerID]      = [initialPrice]
        self.stockBid[tickerID]        = [self.setBid(self.stockPrice[tickerID])]
        self.stockAsk[tickerID]        = [self.setAsk(self.stockPrice[tickerID] )]
        self.stockSpread[tickerID]     = [self.stockAsk[tickerID] - self.stockBid[tickerID]]

        



        #We set the entries at date of IPO to the initial values

        #self.stockInventory[tickerID].values[-1] = outstandingShares
        #self.stockPrice[tickerID].values[-1]     = initialPrice
        #self.stockBid[tickerID].values[-1]       = self.setAsk(self.stockPrice[tickerID].values[-1])
        #self.stockAsk[tickerID].values[-1]       = self.setBid(self.stockPrice[tickerID].values[-1])
        #self.stockSpread[tickerID].values[-1]    = self.stockAsk[tickerID].values[-1]-self.stockBid[tickerID].values[-1]

        #At IPO we assume the marketMaker/Underwriter spends money through purchasing all shares issued by the underlying company
        #We update the marketMaker's wealth at that date accordingly
        wealthUpdate =  - (outstandingShares*initialPrice)
        self.balanceSheet = [wealthUpdate]








    def setRiskFreeRate(self,riskFreeRate):
        self.riskFreeRate = riskFreeRate





    def updateBlanceSheet(self):
        print()




    def receiveOrders(self, demand):
        self.setPrice(demand)
       




    def setPrice(self, demand):
        self.stockPrice.loc[len(self.stockPrice)] = self.stockPrice.iloc[-1] + 0.002*np.array(demand)
       


        
    def setAsk(self, stockPrice):
        return stockPrice
        




    def setBid(self, stockPrice):
        return stockPrice




    def sendQoutes(self):
        return self.stockPrice
        #return self.stockBid.pop(), self.stockAsk.pop()
