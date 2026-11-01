# Agent quick-start: one-page procedure

Paste this into your agent's instructions, together with `RULEBOOK.md`.

```
When asked for a technical-analysis view on a stock:

1. Fetch data (TradingView MCP):
   mcp-tv-get-ohlcv(symbol=<EXCH:TICKER>, interval="1D", count=300, format="columns")
   mcp-tv-get-ohlcv(symbol="AMEX:SPY",    interval="1D", count=300, format="columns")
   If the market is open, ignore the still-forming last bar.

2. Compute the rulebook verdict.
   - If you can run code: save each response's "bars" object to stock.json / spy.json, then run
       python -m tagym.live stock.json spy.json --symbol <EXCH:TICKER> [--drop-last]
     from ta-rulebook/platform, and use its JSON.
   - Otherwise: compute the features in RULEBOOK §1.2 by hand and apply §2 → §3 → §4 → §5 in order.

3. Report:
   - signal (BULLISH / BEARISH / NO_SIGNAL) and decision row (D1–D6);
   - the three layers (regime, health, timing);
   - risk: p(≥20% fall in 60d), risk_flag, ATR%;
   - confidence, invalidation level, any A1 warning;
   - anything you noticed that RULEBOOK §6 says is NOT a signal, listed under "ignored_noise".

4. Never:
   - upgrade a signal because of a candlestick, chart pattern, indicator cross, Fibonacci level,
     support/resistance, divergence, volume spike, ICT/SMC concept, or TradingView Buy/Sell rating;
   - call a top-RS stock BULLISH while SPY is below its 10-month SMA;
   - state confidence "high" or quote YouTube win rates as facts.

5. Remember what the labels mean:
   - BULLISH = lowest crash-risk class (≈6% chance of a ≥20% fall in 60d).
   - BEARISH = broken trend (≈16–21%; worse in bear markets).
   - Neither is a forecast of outperformance; measured excess returns are ≈ 0.
```

## Example verdict (abridged)

```json
{"symbol": "NASDAQ:XYZ", "signal": "BULLISH", "decision_row": "D3",
 "layers": {"regime": "RISK_ON", "health": "HEALTHY", "timing": "PULLBACK"},
 "risk": {"p_drawdown20_60d_est": 0.06, "risk_flag": "LOW", "atr_pct": 1.9},
 "confidence": "medium", "horizon_days": 60,
 "invalidation": "close below SMA200, SMA200 rolls over, >10% off the 52w high, or regime leaves RISK_ON",
 "ignored_noise": ["MACD bullish cross (§6)"]}
```
