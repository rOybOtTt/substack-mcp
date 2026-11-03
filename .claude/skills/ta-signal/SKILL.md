---
name: ta-signal
description: Technical-analysis verdict for a US stock (BULLISH / BEARISH / NO_SIGNAL plus crash-risk estimate) using the evidence-tested rulebook in ta-rulebook/RULEBOOK.md and live TradingView data. Use when asked for a technical view, chart read, "is X technically healthy", trend/risk check, or whether a TA signal exists for a company.
---

# ta-signal — evidence-tested technical verdicts

Follow `ta-rulebook/RULEBOOK.md` (v2.2). This skill is the procedure; the rulebook explains what each part means and the evidence behind it.

## Procedure

1. **Fetch data (TradingView MCP).** Load the tools with ToolSearch if needed.
   - `mcp-tv-get-ohlcv(symbol=<EXCH:TICKER>, interval="1D", count=300, format="columns")`
   - `mcp-tv-get-ohlcv(symbol="AMEX:SPY", interval="1D", count=300, format="columns")`
   - `mcp-tv-get-earnings-calendar(symbols=[<EXCH:TICKER>])`. Take `release_next_date`; it may sit under `out_of_window`.
   - If the market is open, the last bar is still forming: pass `--drop-last`.
2. **Compute.** Save each OHLCV response's `bars` object verbatim to `stock.json` and `spy.json`, then run from `ta-rulebook/platform`:
   ```
   python -m tagym.live stock.json spy.json --symbol <EXCH:TICKER> --next-earnings <YYYY-MM-DD> [--drop-last]
   ```
   If you cannot run code, compute RULEBOOK §1.2 by hand and apply §2 → §3 → §4 → §5 in order.
3. **Report**, in this order:
   - the signal and decision row (D1–D6);
   - the three layers (regime, health, timing);
   - the risk numbers: `p_drawdown20_60d_est`, `p_drop10_10d_est`, `risk_flag` and ATR%;
   - warnings: A1 (strong stock in a weak market), A3 (the close is a 52-week high), E1 (earnings due);
   - confidence and the invalidation level;
   - an `ignored_noise` list.

## Hard rules

- `BULLISH` / `BEARISH` are **risk classes**, not return forecasts. Expected outperformance is ≈ 0; say so.
- Never upgrade a signal because of candlesticks, chart patterns, indicator crosses, Fibonacci levels, support/resistance, divergences, volume spikes, ICT/SMC ideas, post-earnings drift, or TradingView's Buy/Sell rating. All of them were tested and showed no robust edge (RULEBOOK §6).
- Never call BULLISH a stock that is a top relative-strength name while SPY is below its 10-month SMA (A1).
- Never say "safe": market-wide shocks (for example COVID in 2020) hit the BULLISH class too.
- Confidence is `low` or `medium`, never `high`. Never quote YouTube win rates as facts.
- Intraday requests (scalps, day trades, holds of minutes to hours): say no intraday rule passed testing after costs (RULEBOOK §12), give no intraday BULLISH/BEARISH call, and answer with the daily verdict and risk context. Put VWAP, opening-range, intraday RSI/EMA and SMC/ICT ideas under `ignored_noise`.
