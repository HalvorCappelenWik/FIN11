from AlgorithmImports import *
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer

class MyAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2011, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)
        
        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol
        
        self.entry_price = None
        self.stop_loss_percent = 0.02  # 2%
        self.take_profit_percent = 0.05  # 5%
        
        self.Schedule.On(self.DateRules.EveryDay(self.tsla),
        self.TimeRules.BeforeMarketClose(self.tsla, 15), self.ExitPositions)



    def OnData(self, data):
        if not self.tsla in data or not self.musk in data:
            return
        
        price = self.Securities[self.tsla].Price
        score = data[self.musk].Value
        content = data[self.musk].Tweet
        
        # Check for stop-loss and take-profit conditions
        if self.entry_price is not None:
            stop_loss_price = self.entry_price * (1 - self.stop_loss_percent)
            take_profit_price = self.entry_price * (1 + self.take_profit_percent)
            
            if price <= stop_loss_price or price >= take_profit_price:
                self.Liquidate()
                self.Debug("Position closed due to stop-loss/take-profit. Current Price: {:.2f}, Entry Price: {:.2f}, Stop-Loss: {:.2f}, Take-Profit: {:.2f}".format(price, self.entry_price, stop_loss_price, take_profit_price))
                self.entry_price = None

        if score > 0.75:
            self.SetHoldings(self.tsla, 1)
            self.entry_price = price  
        elif score < -0.75:
            self.SetHoldings(self.tsla, -1)
            self.entry_price = price  

        if abs(score) > 0.5:
            self.Log("Score: {:.2f}, Tweet: {}".format(score, content))

    # Function to exit positions
    def ExitPositions(self):
        self.Liquidate()
        self.entry_price = None  # Reset entry price

# Class inheriting from PythonData
class MuskTweet(PythonData):
    # An instance of SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Fetching data from MuskTweetsPreProcessed.csv
    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/scl/fi/jg8jhjlz5syeewyzdjic9/Tweets_Processed_EST.csv?rlkey=481fnuk8xc05dp5cq6qr1j8ht&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile)

    # Reading data from MuskTweetsPreProcessed.csv
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
