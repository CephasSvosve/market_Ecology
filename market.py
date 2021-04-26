from trader import trader
from assets import security
from underwriters import marketMaker
from marketWatch import watch
import pandas as pd

class market:




    #we setup a market

    marketMaker12345 =marketMaker()
   

    AAPL           = marketMaker12345.IPO('AAPL', 1.80, 298333)
    KO             = marketMaker12345.IPO('KO', 1.79, 300000)
    JNJ            = marketMaker12345.IPO('JNJ',1.50,358000)



    #GS             = marketMaker12345.IPO('GS', 30.5, 600000) 
    #ADXN           = marketMaker12345.IPO('ADXV', 22.34, 80000)
    #IMRA           = marketMaker12345.IPO('IMRA', 45.63, 20000)




    valueTrader123 = trader('valueTrader',4,1,10000, marketMaker12345)
    trendFollower  = trader('trendFollower',1,1,10000, marketMaker12345)
    passiveTrader  = trader('passiveTrader',4,1,10000, marketMaker12345)
    noiseTrader    = trader('noiseTrader',1,1,100000, marketMaker12345)
    Traders        = [valueTrader123,trendFollower,passiveTrader,noiseTrader ]
    clock          = watch()

    

    marketMaker12345.setRiskFreeRate(0.02)








    #we generate market activity
    if __name__ == '__main__':
        clock.start()

        while clock.time() < 20:
            qoutes = marketMaker12345.sendQoutes()
            Orders = 0
            for trader in Traders:
                trader.receiveQoutes(qoutes,clock.time())
                Orders += trader.respond()


            marketMaker12345.receiveOrders(Orders)

            clock.tick()

        
        marketMaker12345.stockPrice.to_csv('Update.csv')
        print('---------------------')
        print(marketMaker12345.stockPrice)
        print('---------------------')
        #print(valueTrader123.numberofshares)
        print('---------------------')
        print(Orders)
        print('---------------------')
        #print(valueTrader1.balanceSheet)
        print('---------------------')
        #print(valueTrader1.cashAccount)
        print('---------------------')
        #print(valueTrader1.cashFlow)

    




