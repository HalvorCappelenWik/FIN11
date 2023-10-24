#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime, timedelta
from nltk.sentiment import SentimentIntensityAnalyzer

class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
            
        #Start and end dates for backtest 
        self.SetStartDate(2012, 11, 1)
        self.SetEndDate(2017, 1, 1)

        #Starting cash for backtest, i.e algoritmen starter med en portefølje på $100,000
        self.SetCash(100000)

        #Legger til TSLA stock til algoritmen
        #Vi har "Resolution.Minute" -> Det betyr at vi får prisdata hvert minutt. Kan endre til tick/sec/minute/hour/day 
        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol

        #Vår egen data av tweets fra Elon Musk, Resulution.Minute (algoritme sjekker for data hvert miunutt)
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol

        #Går ut av posisjoner 15 minutter før markedet stenger hver dag
        self.Schedule.On(self.DateRules.EveryDay(self.tsla),
        self.TimeRules.BeforeMarketClose(self.tsla, 15), self.ExitPositions)


    #OnData funksjonen blir kalt hver gang vi får ny data fra vår datakilde
    def OnData(self, data):
        
        if self.musk in data:
            #Henter ut sentiment score og tweet content fra MuskTweet klassen
            score = data[self.musk].Value
            content = data[self.musk].Tweet

            #Hvis score er over 0.5, kjøp TSLA, hvis score er under -0.5, selg TSLA
            #Positiv score betyr positiv sentiment, negativ score betyr negativ sentiment
            #Hvis bare litt poisitiv/negativ sentiment, ikke gjør noe. 
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

    #En instans av SentimentIntensityAnalyzer. 
    #SentimentIntensityAnalyzer er en del av nltk.sentiment, som er en del av Natural Language Toolkit (nltk)
    #Her kan man nok prøve ulike sentimentanalyse modeller for å se hvilken som gir best resultat. 
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