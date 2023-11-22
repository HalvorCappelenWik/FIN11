from datetime import datetime, timedelta
from AlgorithmImports import *

class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2023, 6, 1)
        self.SetCash(100000)
        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol

    def OnData(self, data):
        if self.musk in data:
            score = data[self.musk].Value
            content = data[self.musk].Tweet

            if score == 1:
                self.SetHoldings(self.tsla, 1)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))
                self.Log("Score: " + str(score) + ", Tweet: " + content)

            elif score == -1:
                self.SetHoldings(self.tsla, -1)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=1))
                self.Log("Score: " + str(score) + ", Tweet: " + content)


    def ScheduleLiquidation(self, liquidation_time):
        self.Schedule.On(self.DateRules.EveryDay(self.tsla), self.TimeRules.At(liquidation_time.time()), self.ExitPositions)

    def ExitPositions(self):
        self.Liquidate()

class MuskTweet(PythonData):
    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/scl/fi/kbklj6e4irxak77et4sjw/final_dataset2.csv?rlkey=aqsvbw4pjrqe9wa9phqx4zw56&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile);

    def Reader(self, config, line, date, isLive):
        if not (line.strip() and line[0].isdigit()):
            return None

        data = line.split(',')
        tweet = MuskTweet()

        try:
            tweet.Symbol = config.Symbol
            tweet.Time = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=1) 
            content = data[1].lower()
            tweet.Value = int (data[2]) 
            tweet["Tweet"] = str(content)
            
        except ValueError:
            return None
        
        return tweet
