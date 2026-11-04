# ta-rulebook — an evidence-tested technical-analysis rulebook for agents

**Start here:** [`RULEBOOK.md`](RULEBOOK.md) is the rulebook your agent should load. It tells the agent when a technical-analysis signal exists for a company and when it does not.

## What's in this folder

| Path | What it is |
|---|---|
| `RULEBOOK.md` | **The deliverable.** Decision procedure (market regime → stock health → timing → decision table), the NOT-a-signal list, avoid rules, risk rules, output JSON schema, and TradingView MCP instructions. |
| `AGENT_QUICKSTART.md` | One-page procedure to paste into your agent's instructions: the TradingView MCP calls, the engine call, the report fields and the hard "never" rules. |
| `BELIEFS_VS_EVIDENCE.md` | What the books, YouTube's most-viewed teachers and the academic literature *believe*, next to what the backtests *measured*. |
| `experiments/ITERATION_LOG.md` | Every feedback-loop iteration: the hypothesis, the test, the result, and the decision. Includes all 246 rule-level tests. |
| `experiments/results/` | Raw results: `ledger.jsonl` (every rule test), CSVs for timing, risk, RL, ML, exits, YouTube systems, the fine-tuning grid, and the final locked test. |
| `experiments/test_access_log.md` | Audit trail of every access to the locked out-of-sample data. |
| `paper/` | **Forward paper trading**, run by the scheduled task "TA rulebook daily paper-trading" (weekdays 18:23 New York). To save its results, the task needs repository roybottt/substack-mcp selected with push access, and ideally the TradingView connector (otherwise it falls back to yfinance for earnings dates); set both in the claude.ai routines settings. Contents: `watchlist.csv` (98 stocks), `journal.csv` (daily verdicts), `SCOREBOARD.md` (realized vs expected crash rates), `integrity_log.csv` (TradingView cross-checks). |
| `demo/` | **Demo week, Nov 2–6 2026.** A $100k simulated long-only account run mechanically by the rulebook (`platform/tagym/demo.py`).
Each weekday runs at 08:23 (pre-open), 12:23 (mid-day), 15:23 (pre-close) and 18:23 (after close), New York time.
Contents: `DEMO_REPORT.md`, `trades.csv`, `equity.csv` (vs SPY), `flips.csv` (unfinished-bar reads vs the evening verdict), `decision_log.csv` (every action with its rule id), `marks.csv` (mark-to-market at every run) and `dashboard/` (JSON rows for the tracker dashboard). |
| Tracker dashboard | A private claude.ai dashboard ("TA Demo Tracker") drawn from `demo/dashboard/*.json`: equity vs SPY at every run, positions and queued orders, fills and slippage, intraday flip rate, the latest verdicts and their calibration, and the decision log. Each scheduled run re-exports the JSON (`python -m tagym.dashboard`) and refreshes the dashboard's files. |
| `PLAN_30D.md` | **30-day improvement program (Nov 4 – Dec 4 2026)**, pre-registered before any forward data: what is frozen, the verdict bars, the weekly review routine and the gates for editing the rulebook. |
| `intraday/` | **Hourly intraday forward test** (from Nov 2 2026), run by the scheduled task "TA intraday hourly window" (weekdays 09:30-15:30 New York, one 20-minute window per hour: decisions at xx:35/40/45, flat at xx:55, simulated fills, $1,000 units, 2.5 bps per side). Contents: `trades.csv`, `sessions.csv`, `log.csv`, `REPORT.md` (each rule live vs backtest) and `dashboard/` (JSON for the Intraday tab of the tracker). |
| `../.claude/skills/ta-signal/SKILL.md` | Claude skill: the agent procedure (TradingView calls → engine → report). |
| `experiments/live_journal_2026-11-01.md` | The rulebook applied to live TradingView data, as forward predictions to be scored later. |
| `blind_tests/` | Anonymised blind cases, the agents' answers, scores, and the agents' feedback on rulebook ambiguities. |
| `research/books/` | Rule extractions from 6 classic books: Hamilton, Nelson, Lefèvre/Livermore, Selden and Wyckoff read in full; Schabacker's trading half (Ch. XIX–XXVII) read in full. Plus a survey of the modern canon (Murphy, Edwards & Magee, Bulkowski, Nison, Weinstein, O'Neil, Minervini, Elder, Wilder, Bollinger, Aronson, Connors). |
| `research/academic_evidence.md` | 25 papers and themes with effect sizes, and an A–D evidence grade per TA family. |
| `research/videos/` | The 300 most-viewed TA videos (519M views, 169 h), a topic and channel profile, the creators' beliefs and claimed-performance strategies, and scripts to fetch and analyse transcripts on your own machine. |
| `platform/tagym/` | **TA Gym**, the backtesting and feedback-loop platform (Python). See below. |

## TA Gym (platform/tagym)

| Module | Role |
|---|---|
| `data.py` | yfinance download (S&P 1500 + ETFs + indices), cleaning, tradeability mask |
| `indicators.py`, `features.py` | vectorised, look-ahead-free indicators; cached feature store |
| `signals.py`, `signals_books.py`, `signals_regime.py`, `patterns.py` | 123 coded rules: popular TA, the books, regime/confluence variants, YouTube systems, ZigZag chart patterns |
| `evaluate.py`, `run.py` | event studies (excess vs universe and vs a volatility-matched benchmark, date-clustered Newey-West t), calendar-time portfolios, trade simulation, train/valid/locked-test splits, pre-registered verdicts, ledger |
| `rl.py` | two online reinforcement-learning agents (tabular Thompson bandit; Bayesian linear Thompson bandit) |
| `ml.py` | walk-forward gradient-boosting ceiling test |
| `timing.py`, `dow.py` | index/ETF regime tests and Dow Theory |
| `diagnose.py`, `exits.py` | risk-state analysis and stop/exit tests |
| `rulebook_engine.py`, `rb_eval.py` | the rulebook as code (for backtests) and its evaluation |
| `live.py` | **the rulebook applied to live TradingView OHLCV** (`python -m tagym.live stock.json spy.json`) |
| `blind.py` | anonymised blind-case generator and scorer |
| `final_test.py` | the one-time locked out-of-sample test |
| `earnings.py`, `earn_rules.py`, `final_earnings.py` | earnings calendar (EODHD, 128k events), earnings-risk flag E1, post-earnings-drift tests and their locked test |
| `delisted.py` | survivorship check on stocks that were later delisted (EODHD) |
| `overlay.py` | fast crash-overlay candidates (rejected) |
| `paper.py` | daily paper-trading journal, TradingView cross-check log, automatic scoring |
| `demo.py`, `alpaca.py` | demo-week portfolio (simulated or Alpaca paper account) |
| `dashboard.py` | exports the demo and paper results as JSON rows for the tracker dashboard |
| `intraday_bt.py` | intraday backtest: 10 pre-registered rules in xx:35-xx:55 windows on 60 days of 5-minute bars |
| `intraday_fwd.py` | nightly replay of every intraday window on that day's 5-minute bars; forward ledger, verdict bars, `intraday/FORWARD_REPORT.md` |
| `intraday.py` | the hourly 20-minute paper trader; uses the backtest's own signal code (`bar_signals`) |
| `tests/` | pytest unit tests for the agent engine (`python -m pytest -q tests`) |

Reproduce:

```bash
pip install yfinance pandas numpy scipy scikit-learn pyarrow
cd platform
python -m tagym.data all
python -m tagym.run train batch2
python -m tagym.run valid batch2
```

Set `TAGYM_DATA` to choose where the parquet files go.

## Honest limits

- **Survivorship bias.** The development universe is today's S&P 1500. In v2.2 a sample of 76 later-delisted stocks (EODHD) was checked. The class ordering holds, but absolute crash risk is about 2× higher among those names, and dip-buying looks worse. See RULEBOOK §3.
- **US equities, daily bars.** The intraday layer (`intraday_bt.py`) found no rule that beats costs in 20-minute windows (60 days of 5-minute bars); nothing here validates forex or crypto TA.
- **No transcripts.** YouTube blocks transcript downloads from cloud servers, so the creators' beliefs come from their written material plus video titles, descriptions and chapters. Run `research/videos/fetch_transcripts_locally.py` on your own machine to add transcripts.
- **Copyrighted books.** Modern copyrighted books were studied through legitimate summaries, author sites and published statistics, not full texts.
