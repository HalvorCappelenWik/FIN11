from datetime import datetime, timedelta
from AlgorithmImports import *

class MyAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2012, 1, 1)
        self.SetEndDate(2023, 6, 1)
        self.SetCash(100000)
        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol
    def OnData(self, data):
        if self.musk in data:
            score = data[self.musk].Value
            content = data[self.musk].Tweet
            quantity = self.CalculateOrderQuantity(self.tsla, score)


            if score == 1:
                self.MarketOrder(self.tsla, quantity)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))

            elif score == -1:
                self.MarketOrder(self.tsla, quantity)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))
    def ScheduleLiquidation(self, liquidation_time):
        self.Schedule.On(self.DateRules.EveryDay(self.tsla), self.TimeRules.At(liquidation_time.time()), self.ExitPositions)
    def ExitPositions(self):
        self.Liquidate()

    def OnOrderEvent(self, orderEvent):
        # This method is called whenever there is an order event
        if orderEvent.Status == OrderStatus.Filled:
            # Get the order from the Transactions object
            order = self.Transactions.GetOrderById(orderEvent.OrderId)
            # Log the order details including the type and the associated fees
            self.Log(f"Order executed: ID: {order.Id}, Type: {order.Type}, Symbol: {order.Symbol}, Quantity: {order.Quantity}. Fees: {orderEvent.OrderFee}")


class MuskTweet(PythonData):
    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/scl/fi/kd7p07s7qheal3dbih589/last_dataset.csv?rlkey=0qqjvg58oy4uopl9g6q7gq2en&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile);
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
