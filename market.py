from trader import trader
from assets import security
from underwriters import marketMaker
from marketWatch import watch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class market:
   

    #marketwatch
    dt             = 1/252
    clock          = watch(dt)

    #we setup a market
    periodOfTrade = 10
    marketMaker   =marketMaker(clock)
    
    marketMaker.randomGenerator(size = int(periodOfTrade/dt), numberOfAssets =2)
    print(marketMaker.dzMatrix.shape)

    autoCorr       = np.matrix([[0.4],
                                [0.5]])
    
    crossSecCorr   =  np.matrix([[1,0.6],
                                [0.6, 1]])



    marketMaker.setCorr(autoCorr, crossSecCorr)


    AAPL           = marketMaker.IPO(0,'AAPL', 132.60, 1000000000,1.2,1.5,0.38)
    JNJ            = marketMaker.IPO(1,'JNJ',163.52,1000000000,1.32,1.9,0.42)

    
    



    
 


    valueTrader123 = trader('valueTrader',63,1,500000000, marketMaker,clock)
    trendFollower  = trader('trendFollower',30,1,500000000, marketMaker,clock)
    passiveTrader  = trader('passiveTrader',63,1,500000000, marketMaker,clock)
    noiseTrader    = trader('noiseTrader',1,1,500000000, marketMaker,clock)
    Traders        = [valueTrader123,trendFollower,passiveTrader,noiseTrader]


    
   

    marketMaker.setRiskFreeRate(0.02)








    #we generate market activity
    if __name__ == '__main__':
        clock.start()

        while clock.time() <= periodOfTrade:        #years
            qoutes = marketMaker.sendQoutes()
            Orders = 0
            for trader in Traders:
                trader.receiveQoutes(qoutes,clock.time())
                Orders += trader.respond()
                


            marketMaker.receiveOrders(Orders)

            clock.tick()

        
        
        output =marketMaker.stockPrice

        def returns(output1,Asset):
            returns= []
            for i in range(1,len(output1[Asset])-1):
                a= (output1[Asset][i+1]/output1[Asset][i])
                returns.append(np.log(a))
            return returns



        #Output
        print(output)
        plt.style.use('seaborn')
        figure, axis = plt.subplots(2, 1)
        axis[0].plot(output['JNJ'], label = 'JNJ')
        axis[0].set_ylabel('Price, ($)')
        axis[0].legend(loc = 'upper left')
        axis[0].plot(output['AAPL'], label = 'AAPL')
        axis[0].set_ylabel('Price, ($)')
        axis[0].legend(loc = 'upper left')
        axis[1].scatter(returns(output,'AAPL'),returns(output,'JNJ') )
        axis[1].set_ylabel('JNJ')
        axis[1].set_xlabel('AAPL')
        axis[1].legend(loc = 'upper left')
        
        plt.show()

     
    




