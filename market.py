from trader import trader
from assets import security
from underwriters import marketMaker
from marketWatch import watch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class market:
   




    #we setup a market

    marketMaker12345 =marketMaker()
   

    AAPL           = marketMaker12345.IPO('AAPL', 132.60, 1000000000)
    JNJ            = marketMaker12345.IPO('JNJ',163.52,1000000000)





    valueTrader123 = trader('valueTrader',63,1,250000000, marketMaker12345)
    trendFollower  = trader('trendFollower',30,1,250000000, marketMaker12345)
    passiveTrader  = trader('passiveTrader',63,1,250000000, marketMaker12345)
    noiseTrader    = trader('noiseTrader',1,1,250000000, marketMaker12345)
    Traders        = [valueTrader123,trendFollower,passiveTrader,noiseTrader ]


    clock          = watch()

    

    marketMaker12345.setRiskFreeRate(0.02)








    #we generate market activity
    if __name__ == '__main__':
        clock.start()

        while clock.time() < 10:
            qoutes = marketMaker12345.sendQoutes()
            Orders = 0
            for trader in Traders:
                trader.receiveQoutes(qoutes,clock.time())
                Orders += trader.respond()
                


            marketMaker12345.receiveOrders(Orders)

            clock.tick()

        
        
        output =marketMaker12345.stockPrice

        def returns(output1,Asset):
            returns= []
            for i in range(1,len(output1[Asset])-1):
                a= (output1[Asset][i+1]/output1[Asset][i])
                returns.append(np.log(a))
            return returns



        #Output
        print(output)
        plt.style.use('seaborn')
        figure, axis = plt.subplots(4, 1)
        axis[0].plot(output['JNJ'], label = 'JNJ')
        axis[0].set_ylabel('Price, ($)')
        axis[0].legend(loc = 'upper left')
        axis[1].plot(output['AAPL'], label = 'AAPL')
        axis[1].set_ylabel('Price, ($)')
        axis[1].legend(loc = 'upper left')
        axis[2].plot(returns(output,'AAPL'), label = 'AAPL')
        axis[2].set_ylabel('Return')
        axis[2].set_xlabel('Day, t')
        axis[2].legend(loc = 'upper left')
        
        axis[3].plot(returns(output,'JNJ'), label = 'JNJ')
        axis[3].set_ylabel('Return')
        axis[3].set_xlabel('Day, t')
        axis[3].legend(loc = 'upper left')
        plt.show()

     
    




