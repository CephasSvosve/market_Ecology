import numpy as np
import pandas as pd 
from assets import security

class marketMaker:
    def __init__(self):
        self.stockInventory = pd.DataFrame()
        self.stockPrice     = pd.DataFrame()
        self.stockBid       = pd.DataFrame()
        self.stockAsk       = pd.DataFrame()
        self.stockSpread    = pd.DataFrame()
        self.balanceSheet   = []
        self.riskFreeRate   = self.setRiskFreeRate
        

    #This is a method that we use to introduce securities into the market
    def IPO(self,tickerNumber,tickerID, initialPrice, outstandingShares):

        newAsset = security(tickerNumber,tickerID,(initialPrice * outstandingShares),outstandingShares)

        #We add the newstock to the stockInventory dataframe and update other dataframes accordingly
        #We set all dataframe entries prior to the IPO to zero to avoid missing entry errors

        self.stockInventory[tickerID]  = [0 for x in range(len(self.stockInventory))]
        self.stockPrice[tickerID]      = [0 for x in range(len(self.stockPrice))]
        self.stockBid[tickerID]        = [0 for x in range(len(self.stockBid))]
        self.stockAsk[tickerID]        = [0 for x in range(len(self.stockAsk))]
        self.stockSpread[tickerID]     = [0 for x in range(len(self.stockSpread))]

        #We set the entries at date of IPO to the initial values

        self.stockInventory[tickerID].values[-1] = outstandingShares
        self.stockPrice[tickerID].values[-1]     = initialPrice
        self.stockBid[tickerID].values[-1]       = self.setAsk(self.stockPrice[tickerID].values[-1])
        self.stockAsk[tickerID].values[-1]       = self.setBid(self.stockPrice[tickerID].values[-1])
        self.stockSpread[tickerID].values[-1]    = self.stockAsk[tickerID].values[-1]-self.stockBid[tickerID].values[-1]

        #At IPO we assume the marketMaker/Underwriter spends money through purchasing all shares issued by the underlying company
        #We update the marketMaker's wealth at that date accordingly
        wealthUpdate = self.balanceSheet[-1] - (outstandingShares*initialPrice)
        self.balanceSheet[-1] = wealthUpdate

    def setRiskFreeRate(riskFreeRate):
        return riskFreeRate

    def updateBlanceSheet():
        print()
    def receiveOrders(self):
        print()
    def setPrice(self):
        print()
    def setAsk(self, stockPrice):
        print()
    def setBid(self):
        print()
    def sendQoutes(self):
        return self.stockPrice
        return self.stockBid.pop(), self.stockAsk.pop()
