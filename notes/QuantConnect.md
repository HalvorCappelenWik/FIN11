# Trading in Quantconnect

## Methods 
* self.rebalance()
* self.setBenchmark()
* self.setbrokeragemodel() -> 
* AccountType.margin or AccountType.cash -> should we allow using leverage? 
* self:MarketOrder 
* self.LimitOrder
* self.StopMarketOrder <- stoploss with market order 
* self.StopLimitOrder <- stoploss with limit order 
* Self.marketOnClose
* Self.marketOnOpen 

## Concepts
* Datatypes: 
    * Tick data: data for single point in time 
    * Bar data: covers a period, which have both an start time and end time. Lean only allows us to use endtime of a bar! This restriction ensures that we dont use future data (avoid look-ahead bias)
* TradeBars: Built by consolidating trades from exchanges. 
* QuoteBars: Built by consolidating bid and ask prices from exchanges. 

## Properties of a asset
* Value 
* SecurityType 
* Market -> forex, equities 
* HasUnderlying -> is the asset a derivate? 
* Date -> ealiest listing date for equities // expiration date for futures and options 
* OptionType 
* OptionRight (call/put)
* StrikePrice


## Properties of self.Portfolio.Invested:
* Cash 
* UnsettledCash 
* TotalFees 
* TotalHoldingsValue 
* MarginRemaing
* TotalMarginUsed 
* TotalPortfolioValue
* TotalProfit
* TotalUnrealizedProfit

