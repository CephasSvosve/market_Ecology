import numpy as np
import pandas as pd 
from dataFrameControl import dfControl as df


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
        self.stockBid[tickerID]        = [self.setBid(df.getColumn(tickerID,self.stockPrice,lastValueOnly =True))]
        self.stockAsk[tickerID]        = [self.setAsk(df.getColumn(tickerID,self.stockPrice,lastValueOnly =True))]
        self.stockSpread[tickerID]     = [self.stockAsk[tickerID] - self.stockBid[tickerID]]

        

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
        #set new price depending on excess demand
        newPrice  = np.random.normal(df.getLastRow(self.stockPrice),1)
        df.appendNextRow(self.stockPrice,newPrice)
        
        #adjust inventory
        newInventory  = df.getLastRow(self.stockInventory) + self.newIssue()   #Incase we want to include issuance of additional shares inter period
        df.appendNextRow(self.stockInventory,newInventory)
        
    def setAsk(self, stockPrice):
        return stockPrice
        




    def setBid(self, stockPrice):
        return stockPrice




    def sendQoutes(self):
        return self.stockPrice
        #return self.stockBid.pop(), self.stockAsk.pop()


    def newIssue(self,tickerID,numberofshares):
        newShares = []
        for ticker in self.stockInventory.columns:
            if (ticker == tickerID):
                a = df.getColumn( columnName=ticker, dataFrame = self.stockInventory, lastValueOnly = True) + numberofshares
            else:
                a = 0
            newShares.append(a)

        return np.array(newShares)


    
    def newIssue(self):
        newShares = []
        for tickerID in self.stockInventory.columns:
            a = 0
            newShares.append(a)

        return np.array(newShares)


    
        