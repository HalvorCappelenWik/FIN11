## Workflow in algotrading 
Research -> Coding -> Backtesting -> Optimizing -> Paper trading -> Live trading -> Monotoring 


### Exampel on sentiment analysis:
    tweet = "first profitable q for tesla thanks to awesome customers & hard work by a super dedicated team" 
    sia.polarity_scores(tweet) = {neg: 0.051, neu: 0.331, pos: 0.618, compound: 0.9468}

    tweet = "not all good news. virginia dmv commissioner just denied tesla dealer license" 
    sia.polarity_scores(tweet) = {neg: 0.347, neu: 0.653, pos: 0.0, compound: -0.6492}


### Other notes 
* sentimentanalyzer is not optimized for twitter text data?
* Dont use to many fixed parameters. If so always be able to explain why this "value" 
