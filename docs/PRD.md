# WantGoo Spider PRD (Product Requirements Document)

## 1. Project Overview
Project Name: `wantgoo_spider`
Goal: Build an automated web crawler to fetch after-market institutional chips and market breadth data from WantGoo (玩股網). The output will be a structured JSON file used by AI trading agents.

## 2. MVP Scope (Phase 1)
According to the requirements, Phase 1 only focuses on **After-Market Data** (Modules 2, 3, 4). Real-time futures data (Module 1) is deferred to Phase 2.

### Module 2: Retail Sentiment Indicators (散戶動向指標)
*   **Target**: Micro TSMC / Mini TSMC Retail Long-Short Ratio.
*   **Fields**:
    *   `retail_net_position`: 散戶淨部位 (positive for net long, negative for net short)
    *   `retail_long_short_ratio`: 散戶多空比百分比 (%)
    *   `daily_change`: 相較前一日增減量

### Module 3: Institutional Chips (法人主力籌碼)
*   **Target**: Three major institutional investors / Large traders (Top 5 / Top 10 specific).
*   **Fields**:
    *   `foreign_net_position`: 外資台指期未平倉淨部位口數
    *   `top10_specific_net_position`: 前十大特定法人未平倉淨部位口數
    *   `daily_change`: 相較前一日增減量

### Module 4: Market Breadth (市場廣度)
*   **Target**: TAIEX market health.
*   **Fields**:
    *   `market_up_down_ratio`: 大盤漲跌家數比例
    *   `moving_average_alignment`: 多頭排列家數比例 vs 空頭排列家數比例

## 3. Output Format (JSON Schema)
The crawler must produce a single JSON file (e.g., `wantgoo_market_data.json`) with the following structure for MVP:

```json
{
  "global_timestamp": "2026-05-22T23:50:00+08:00",
  "data": {
    "sentiment_indicators": {
      "updated_at": "2026-05-22T15:30:00+08:00",
      "status": "ok",
      "micro_tx_retail_ratio": {
        "net_position": 2500,
        "ratio_pct": 15.2,
        "daily_change": 500
      }
    },
    "institutional_chips": {
      "updated_at": "2026-05-22T15:30:00+08:00",
      "status": "ok",
      "foreign_tx_net_position": -5200,
      "foreign_daily_change": -1200,
      "top10_specific_net_position": 1200,
      "top10_daily_change": 300
    },
    "market_breadth": {
      "updated_at": "2026-05-22T16:00:00+08:00",
      "status": "ok",
      "advancing_issues": 650,
      "declining_issues": 230,
      "bullish_alignment_pct": 45.5,
      "bearish_alignment_pct": 30.2
    }
  }
}
```

## 4. Technical Constraints & Red Lines
1.  **Architecture**: Prefer `requests` (underlying API or HTML parsing). Only use `playwright` if absolutely necessary.
2.  **Anti-Fragile (防呆)**: If a field is missing or page structure changes, set `status` to `"error"` (or `"waiting_data"`). ZERO TOLERANCE for silently returning `null` or `0`.
3.  **Testing**: Unit tests must NOT hit the live WantGoo server. `pytest` MUST use mocking (e.g., local HTML fixtures or `responses`).
4.  **Version Control**: Strict 2-phase release process. PR submitter must be Bot. `README.md` must be at the root.