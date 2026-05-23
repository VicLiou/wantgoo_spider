# 系統架構規格 (System Architecture Specification)

## 專案名稱
wantgoo_spider

## 1. 系統架構總覽
本專案為自動化網路爬蟲，專注於抓取玩股網 (WantGoo) 盤後籌碼與市場廣度資訊。為符合專案輕量化與效能要求，**強制規定使用 `requests` 模組**作為 HTTP 請求核心，若需解析 HTML 則搭配 `BeautifulSoup4` (或其他輕量解析庫)，拒絕使用耗費資源的 `playwright` 或 `selenium`。爬取結果最終實體化為結構化 JSON 檔案，供應 AI 交易代理人 (Trading Agents) 使用。

## 2. 目錄結構 (Folder Structure)
遵循 Clean Architecture 原則，切割資料抓取、解析、檔案輸出與測試：

```text
/home/ddad/projects/wantgoo_spider/
├── README.md               # 專案根目錄說明文件
├── docs/                   # 系統與需求規格區
│   ├── PRD.md
│   ├── architecture_spec.md
│   └── acceptance_criteria.md
├── src/                    # 應用程式原始碼
│   ├── main.py             # 程式進入點 (排程或單次執行)
│   ├── fetcher/            # 負責處理 requests HTTP 請求與防護機制
│   ├── parsers/            # 負責將 HTML/API 回傳資料解析為結構化 Dict
│   └── exporter.py         # 負責將資料格式化並輸出為 JSON 檔案
├── tests/                  # 測試區
│   ├── fixtures/           # 放置 Mock 用的靜態 HTML 或 API JSON
│   └── test_parsers.py     # pytest 單元測試
└── requirements.txt        # 專案依賴 (requests, beautifulsoup4, pytest, responses 等)
```

## 3. 模組介面 (Module Interfaces)
### 3.1 爬蟲請求模組 (`src/fetcher`)
- **技術棧**: `requests`
- **職責**: 負責與玩股網伺服器進行 HTTP 通訊。封裝重試機制 (Retry)、Timeout 控制與 Headers (如 User-Agent) 偽裝。
- **錯誤處理**: 發生連線錯誤或 HTTP 非 200 時，不可崩潰，應記錄錯誤狀態回傳給解析層。

### 3.2 資料解析模組 (`src/parsers/`)
- **模組劃分**: 
  - `sentiment_parser`: 負責解析微台指/小台指散戶多空比 (Module 2)。
  - `institutional_parser`: 負責解析三大法人與前十大特定法人部位 (Module 3)。
  - `breadth_parser`: 負責解析大盤漲跌家數與多空排列比例 (Module 4)。
- **防呆機制**: 欄位遺失或網頁結構變更時，必須將該模組的 `status` 設為 `"error"` 或 `"waiting_data"`，嚴禁回傳預設值如 `null` 或 `0`，避免誤導 AI 代理人。

### 3.3 輸出模組 (`src/exporter.py`)
- **職責**: 將解析後的 Python Dictionary 轉譯為最終 JSON 格式，並寫入本機檔案 `wantgoo_market_data.json`。

## 4. 資料庫 Schema (Database Schema)
本專案無關聯式資料庫。所有資料以本機 JSON 檔案落地，Schema 完全依照 PRD 中所定義的樹狀結構 (包含 `global_timestamp` 與 `data` 節點)，確保時間戳記採用 ISO 8601 (含時區) 格式。
