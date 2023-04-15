//@version=4
strategy("Consolidation Breakout Strategy")

// Parameters
atr_length = input(title="ATR Length", type=input.integer, defval=14)
atr_multiplier = input(title="ATR Multiplier", type=input.float, defval=2.0)
stop_loss = input(title="Stop Loss (%)", type=input.float, defval=1.0)

// Calculate the ATR
atr = atr(atr_length)

// Calculate the upper and lower boundaries of the consolidation pattern
consolidation_upper = high + atr * atr_multiplier
consolidation_lower = low - atr * atr_multiplier

// Calculate the MACD
fast_length = input(title="Fast Length", type=input.integer, defval=12)
slow_length = input(title="Slow Length", type=input.integer, defval=26)
signal_length = input(title="Signal Length", type=input.integer, defval=9)
(macd, signal, _) = macd(close, fast_length, slow_length, signal_length)

// Determine whether the market is consolidating or trending
is_consolidating = low > consolidation_lower and high < consolidation_upper
is_trending = low < consolidation_lower or high > consolidation_upper

// Determine whether there is a breakout
is_breakout = crossover(macd, signal) and is_trending

// Enter long position if there is a breakout
if is_breakout
    strategy.entry("Long", strategy.long)

// Exit long position if the market is no longer trending
if not is_trending
    strategy.close("Long")

// Implement stop-loss order
stop = close * (1 - stop_loss / 100)
strategy.exit("Long Stop", "Long", stop=stop, qty_percent=100)

