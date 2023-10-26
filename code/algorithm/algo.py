#region imports
from AlgorithmImports import *
#endregion
from nltk.sentiment import SentimentIntensityAnalyzer
import datetime

class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2011, 1, 1)
        self.SetEndDate(2023, 6, 28)
        self.SetCash(100000)
        

        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol
        
        self.Schedule.On(self.DateRules.EveryDay(self.tsla),
        self.TimeRules.BeforeMarketClose(self.tsla, 15), self.ExitPositions)


    def OnData(self, data):

        if self.musk in data:
            score = data[self.musk].Value
            content = data[self.musk].Tweet
            
            if score > 0.5:
                self.SetHoldings(self.tsla, 1)
            elif score < -0.5:
                self.SetHoldings(self.tsla, -1)

            #Linje for å logge tweet
            if abs(score) > 0.5:
                self.Log("Score: " + str(score) + ", Tweet: " + content)

                
    def ExitPositions(self):
        self.Liquidate()


class MuskTweet(PythonData):

    sia = SentimentIntensityAnalyzer()

    def GetSource(self, config, date, isLive):
        #Må ha dl=1 for nedlastning av dropbox fil 
        source = "https://www.dropbox.com/scl/fi/b0xn7ma6s531uhd14xgjb/Tweets_Processed_10-23.csv?rlkey=ep44kkwmsr88g88vk6uo2q9oe&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile)

    def Reader(self, config, line, date, isLive):
        if not (line.strip() and line[0].isdigit()):
            return None
        
        data = line.split(',')
        tweet = MuskTweet()
        
        try:
            tweet.Symbol = config.Symbol

            #Endre til +1 sekund? 
            tweet.Time = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=1)
            content = data[1].lower()
            
            if "tsla" in content or "tesla" in content:
                tweet.Value = self.sia.polarity_scores(content)["compound"]
            else:
                tweet.Value = 0
            
            tweet["Tweet"] = str(content)
            
        except ValueError:
            return None
        
        return tweet

