
#Build a stock and give it unique attributes like any company listed on the stock exchange
class security:
    import numpy as np

    def __init__(self,tickerName, marketCapital, outstandingShares, initialPrice):
        self.tickerName        = tickerName
        self.balanceSheet      = []
        self.marketCapital     = [marketCapital]
        self.outstandingShares = [outstandingShares]
        self.marketPrice       = [initialPrice]   
        self.bookValue         = []     
        self.quarterlyDividend = []
        self.dailyDividend     = []
       

    
