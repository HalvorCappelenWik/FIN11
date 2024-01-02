from datetime import datetime, timedelta
from AlgorithmImports import *

class MyAlgorithm(QCAlgorithm):
    def Initialize(self):

        self.SetStartDate(2012, 1, 1)
        
        self.SetEndDate(2023, 8, 1)
        self.SetCash(10000)

        tsla_security = self.AddEquity("TSLA", Resolution.Tick)
        self.tsla = tsla_security.Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Tick).Symbol
        self.SetBrokerageModel(BrokerageName.QuantConnectBrokerage, AccountType.Cash) 
        tsla_security.SetFeeModel(InteractiveBrokersFeeModel())

        self.stopLossPercentage = 0.99 # 1% stop loss
        self.openingPrices = {}  # To track opening prices of positions

    def OnData(self, data):
        if self.musk in data:
            score = data[self.musk].Value
            quantity = self.CalculateOrderQuantity(self.tsla, score)
            if score == 1:
                self.MarketOrder(self.tsla, quantity)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))
            elif score == -1:
                self.MarketOrder(self.tsla, quantity)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))

        # Call the function to check for stop loss
        self.CheckStopLoss(data)

    def CheckStopLoss(self, data):
        for holding in self.Portfolio.Values:
            if holding.Invested:
                symbol = holding.Symbol
                if symbol in data and symbol in self.openingPrices:
                    stopLossPrice = self.openingPrices[symbol] * self.stopLossPercentage
                    if data[symbol].Price <= stopLossPrice:
                        self.Liquidate(symbol)
                        self.Log(f"Stop loss triggered for {symbol} at {data[symbol].Price}")

    def ScheduleLiquidation(self, liquidation_time):
        self.Schedule.On(self.DateRules.EveryDay(self.tsla), self.TimeRules.At(liquidation_time.time()), self.ExitPositions)

    def ExitPositions(self):
        self.Liquidate()

    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status == OrderStatus.Filled:
            order = self.Transactions.GetOrderById(orderEvent.OrderId)
            self.Log(f"Order executed: ID: {order.Id}, Type: {order.Type}, Symbol: {order.Symbol}, Quantity: {order.Quantity}. Fees: {orderEvent.OrderFee}")
            if orderEvent.Direction == OrderDirection.Buy:
                self.openingPrices[order.Symbol] = orderEvent.FillPrice

class MuskTweet(PythonData):
    def GetSource(self, config, date, isLive):
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
            tweet.Value = int(data[2]) 
            tweet["Tweet"] = str(content)
        except ValueError:
            return None
        return tweet




