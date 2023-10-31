
# Important aspects when backetesting 
* Backtest results < Real results 
* When backtesting we make a lot of assumptions about the executions of trades: 
    * Fees, timing, data, availability of assets 
    * Assumptions can be unrealistic 

## Biases

### Overfittting
* The act of fitting your strategy to closely to the backtest data
* At some point the algorithm wont actually make meaningful trading decisions but instead just make certian decisions becasue it knows the backtest data to well. 
* Common mistake:
    * Constantly adjust the algorithm and then backtest to check wheather or not performance is better or worse than before. -> this will create a useless overfitted algorithm! 
    * Should not try to backtest to ofthen
* How to avoid:
    * We devide data into two subsets. Train / Test data. 
    * Try paper trading 

### Look Ahead Bias 

### Survivorhip Bias 