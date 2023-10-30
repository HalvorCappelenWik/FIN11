from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer
from AlgorithmImports import *

class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2023, 6, 1)
        self.SetCash(100000)
        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol

    def OnData(self, data):
        price = self.Securities[self.tsla].Price
        
        if self.musk in data:
            score = data[self.musk].Value
            content = data[self.musk].Tweet

            if score > 0.75:
                self.SetHoldings(self.tsla, 1)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=30))
            elif score < -0.75:
                self.SetHoldings(self.tsla, -1)
                self.ScheduleLiquidation(self.Time + timedelta(minutes=30))

            if abs(score) > 0.5:
                self.Log("Score: " + str(score) + ", Tweet: " + content)

    def ScheduleLiquidation(self, liquidation_time):
        self.Schedule.On(self.DateRules.EveryDay(self.tsla), 
                        self.TimeRules.At(liquidation_time.time()), 
                        self.ExitPositions)


    def ExitPositions(self):
        self.Liquidate()

class MuskTweet(PythonData):
    sia = SentimentIntensityAnalyzer()

    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/scl/fi/jg8jhjlz5syeewyzdjic9/Tweets_Processed_EST.csv?rlkey=481fnuk8xc05dp5cq6qr1j8ht&dl=1"
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
            
            if "tsla" in content or "tesla" in content:
                tweet.Value = self.sia.polarity_scores(content)["compound"]
            else:
                tweet.Value = 0

            tweet["Tweet"] = str(content)
            
        except ValueError:
            return None
        
        return tweet
