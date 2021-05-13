
#Build a stock and give it unique attributes like any company listed on the stock exchange
import numpy as np
import scipy.linalg

from numpy.lib.scimath import sqrt

class security:

    def __init__(self,tickerName, marketCapital, outstandingShares, initialPrice):
        self.tickerName        = tickerName
        self.balanceSheet      = []
        self.marketCapital     = [marketCapital]
        self.outstandingShares = [outstandingShares]
        self.marketPrice       = [initialPrice]   
        self.bookValue         = []     
        self.quarterlyDividend = []
        self.dailyDividend     = []
       
    def dividendPayout(self):
        print()

    def updateRecords(self):
        print()
    
    def computeDividend(self):
        print()
    


    def uncorrelatedRandoms(self,size, numberOfAssets):

        c = np.zeros((numberOfAssets,size))

        for x in range(numberOfAssets):
            c[x] = np.random.normal(0,1,size)


        corrmatrix        = np.corrcoef(c)
        choleskyMtrx      = scipy.linalg.cholesky(corrmatrix, lower = True)
        invcholeskyMtrx   = scipy.linalg.inv(choleskyMtrx)
        uncorrMtrx        = invcholeskyMtrx.dot(c)
            
        return uncorrMtrx



    def temporalCorr(self, autocorrelation, randomNumbers):
        dz     = randomNumbers
        dw     = dz[0]
        
        for i in range(len(dz)-1):
            dx = sqrt(1-autocorrelation**2)*dz[i+1]  +   dw[-1]
            dw.append(dx)
        
        return dw



    def crossCorrelation(self, correlationMatrix, dwMatrix):
        print()
