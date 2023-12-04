from datetime import datetime, timedelta
from AlgorithmImports import *

class MyAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2012, 1, 1)
        self.SetEndDate(2023, 8, 1)
        self.SetCash(10000)
        self.tsla = self.AddEquity("TSLA", Resolution.Tick).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Tick).Symbol

    def OnData(self, data):
        if self.musk in data:
            score = data[self.musk].Value
            quantity = self.CalculateOrderQuantity(self.tsla, score)

            if score == 1:
                self.MarketOrder(self.tsla, quantity)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))
                #self.Log(f"Tweets: {content}, Score: {score}")

            elif score == -1:
                self.MarketOrder(self.tsla, quantity)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))
                #self.Log(f"Tweets: {content}, Score: {score}")

            else:
                None


    def ScheduleLiquidation(self, liquidation_time):
        self.Schedule.On(self.DateRules.EveryDay(self.tsla), self.TimeRules.At(liquidation_time.time()), self.ExitPositions)
    def ExitPositions(self):
        self.Liquidate()
    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status == OrderStatus.Filled:
            order = self.Transactions.GetOrderById(orderEvent.OrderId)
            self.Log(f"Order executed: ID: {order.Id}, Type: {order.Type}, Symbol: {order.Symbol}, Quantity: {order.Quantity}. Fees: {orderEvent.OrderFee}")

class MuskTweet(PythonData):
    def GetSource(self, config, date, isLive):
        # For backtesting, livefeeding of data is not implemented. 
        source = "https://www.dropbox.com/scl/fi/4t6szo6q50piauhwjns6v/final_results_sec.csv?rlkey=mtx8ugpkss6y5lq8u6db9a0f3&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile)
    def Reader(self, config, line, date, isLive):
        if not (line.strip() and line[0].isdigit()):
            return None
        data = line.split(',')
        tweet = MuskTweet()
        try:
            tweet.Symbol = config.Symbol
            tweet.Time = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S') 
            content = data[1].lower()
            tweet.Value = int (data[2]) 
            tweet["Tweet"] = str(content)
            
        except ValueError:
            return None
        
        return tweet


