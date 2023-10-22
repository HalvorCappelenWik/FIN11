# FIN11
FIN11 Term paper: Trading and Market Microstructure. 

* Quantconnet 
* NLTK for sentiment analysis 

### Data
* Tweets 2012-2017 -> https://www.kaggle.com/datasets/kulgen/elon-musks-tweets 
* Tweets 2010-2023 (june) -> https://www.kaggle.com/datasets/aryansingh0909/elon-musk-tweets-updated-daily?rvi=1


### Notes
* Look-ahead bias
* sentimentanalyzer is not optimized for twitter text data?
* Dont use to many fixed parameters. If so always be able to explain why this "value" 


### Exampel on sentiment analysis:
    tweet = "first profitable q for tesla thanks to awesome customers & hard work by a super dedicated team" 
    sia.polarity_scores(tweet) = {neg: 0.051, neu: 0.331, pos: 0.618, compound: 0.9468}

    tweet = "not all good news. virginia dmv commissioner just denied tesla dealer license" 
    sia.polarity_scores(tweet) = {neg: 0.347, neu: 0.653, pos: 0.0, compound: -0.6492}