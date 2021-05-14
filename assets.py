
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

    
    def dividendNoise(self,numberOfAssets,size, autocorrelationMatrix, correlationMatrix):
        dzMatrix      = self.uncorrelatedRandoms(size, numberOfAssets)
        temporalCorr  = self.temporalCorr(autocorrelationMatrix,dzMatrix)
        crossTempCorr = self.crossCorrelation(correlationMatrix,temporalCorr)

        return crossTempCorr

    


    def uncorrelatedRandoms(self,size, numberOfAssets):

        c = np.zeros((numberOfAssets,size))

        for x in range(numberOfAssets):
            c[x] = np.random.normal(0,1,size)


        corrmatrix        = np.corrcoef(c)
        choleskyMtrx      = scipy.linalg.cholesky(corrmatrix, lower = True)
        invcholeskyMtrx   = scipy.linalg.inv(choleskyMtrx)
        uncorrMtrx        = invcholeskyMtrx.dot(c)
            
        return uncorrMtrx



    def temporalCorr(self, autocorrelationMatrix, dzMatrix):
        dz     = dzMatrix
        dw     = np.zeros((len(dz),len(dz[0])))
        
        

        for row in range(len(dz)):
            dw[row][0] = np.random.normal(0,1)
            for column in range(len(dz[row])-1):
                dx = sqrt(1-autocorrelationMatrix[row]**2)*dz[column]  +   autocorrelationMatrix[row]*dw[-1]

                dw[row][column+1] = dx
            
        return dw



    def crossCorrelation(self, correlationMatrix, dwMatrix):
        L = scipy.linalg.cholesky(correlationMatrix, lower=True)
        Z = L.dot(dwMatrix)

        return Z
