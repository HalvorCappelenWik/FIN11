from AlgorithmImports import *
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer

class MyAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetEndDate(2023, 6, 1)
        self.SetCash(100000)

        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol


        self.entry_price = None
        self.stop_loss_percent = 0.02  # 2%



    def OnData(self, data):
        if not self.tsla in data or not self.musk in data:
            return


        price = self.Securities[self.tsla].Price
        score = data[self.musk].Value
        content = data[self.musk].Tweet
        
        # Check for stop-loss and take-profit conditions
        if self.entry_price is not None:
            stop_loss_price = self.entry_price * (1 - self.stop_loss_percent)
            
            if price <= stop_loss_price:
                self.Liquidate()
                self.Debug("Position closed due to stop-loss. Current Price: {:.2f}, Entry Price: {:.2f}, Stop-Loss: {:.2f}".format(price, self.entry_price, stop_loss_price))
                self.entry_price = None

        if score == 1:
            self.SetHoldings(self.tsla, 1)
            self.Log("Score: {:.2f}, Tweet: {}".format(score, content))
            self.entry_price = price
    
        elif score == -1:
            self.SetHoldings(self.tsla, -1)
            self.Log("Score: {:.2f}, Tweet: {}".format(score, content))
            self.entry_price = price
        else:
            None

    # Function to exit positions
    def ExitPositions(self):
        self.Liquidate()
        self.entry_price = None  # Reset entry price

class MuskTweet(PythonData):

    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/scl/fi/tn2m2kwdfmw38utiisdbu/trading_test.csv?rlkey=gg8bx53frbqqwmzso9e3wxbua&dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile);

    def Reader(self, config, line, date, isLive):
        if not (line.strip() and line[0].isdigit()):
            return None
        
        data = line.split(',')
        tweet = MuskTweet()

        try:
            tweet.Symbol = config.Symbol
            tweet.Time = datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S') 
            content = data[5].lower()
            tweet.Value = int (data[6]) 
            tweet["Tweet"] = str(content)
            
        except ValueError:
            return None
        
        return tweet
