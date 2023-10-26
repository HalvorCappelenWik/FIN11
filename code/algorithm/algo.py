#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer

class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
            
        self.SetStartDate(2012, 11, 1) #First tweet 
        self.SetEndDate(2017, 1, 1) #Last tweet

        
        self.SetCash(100000) #OBS må finne et fornuftig beløp å starte med
        self.tsla = self.AddEquity("TSLA", Resolution.Second).Symbol #Resolution = Second 
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol #Our own data of tweets 


        #Må ha strategi på hvor lenge vi skal holde posisjonen. 
        #Finner et gitt antall minutter etter å ha tatt posisjon og så selger vi.
        #Viss en tweet kommer nærmere slutten av dagen, så kan vi ikke vente til neste dag med å selge.

    def OnData(self, data):
        

        if self.musk in data:
            score = data[self.musk].Value
            content = data[self.musk].Tweet

            if score > 0.75:

                #100% av porteføljen blir brukt til å kjøpe TSLA 
                self.SetHoldings(self.tsla, 1)  
            elif score < -0.75:
                #100% av porteføljen blir brukt til å gå short TSLA
                self.SetHoldings(self.tsla, -1)

            #Linje for å logge tweet
            if abs(score) > 0.5:
                self.Log("Score: " + str(score) + ", Tweet: " + content)


    #Funksjon for å gå ut av posisjoner
    def ExitPositions(self):
        self.Liquidate()


#Class inheriting from PythonData
class MuskTweet(PythonData):

    sia = SentimentIntensityAnalyzer()

    #Henter ut data fra MuskTweetsPreProcessed.csv
    def GetSource(self, config, date, isLive):
        source = "https://www.dropbox.com/s/cmi9xcvhh1cbhjl/MuskTweetsPreProcessed.csv?dl=1"
        return SubscriptionDataSource(source, SubscriptionTransportMedium.RemoteFile);


    #Leser data fra MuskTweetsPreProcessed.csv
    def Reader(self, config, line, date, isLive):

        #Hvis linjen er tom eller ikke starter med et tall, returner None (not valid data)
        if not (line.strip() and line[0].isdigit()):
            return None
        
        #Splitter linjen på komma
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