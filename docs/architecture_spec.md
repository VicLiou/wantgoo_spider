# 系統架構規格 (System Architecture Specification) - Phase 2

## 專案名稱
wantgoo_spider

## 1. 系統架構總覽
因應目標網站 (WantGoo) 導入 Cloudflare 防護導致 `requests` 遭遇 HTTP 403 阻擋，本專案 (Phase 2) 進行核心爬取模組升級。架構由同步的 `requests` 全面替換為基於非同步 (Async) 的 `playwright` 無頭瀏覽器 (Headless Browser) 方案。
系統將啟動 Browser Context 模擬真實使用者行為，等待並突破 Cloudflare 驗證後，直接攔截底層 API 回傳的 JSON 封包或進行 DOM 解析，最終依舊實體化為結構化 JSON 檔案，供應 AI 交易代理人使用。

## 2. 目錄結構 (Folder Structure)
```text
/home/ddad/projects/wantgoo_spider/
├── README.md               # 專案根目錄說明文件
├── docs/                   # 系統與需求規格區
│   ├── PRD_Phase2.md
│   ├── architecture_spec.md
│   └── acceptance_criteria.md
├── src/                    # 應用程式原始碼
│   ├── main.py             # 程式進入點 (Async 啟動)
│   ├── fetcher/            # 負責 Playwright 瀏覽器控制與 Cloudflare 繞過
│   ├── parsers/            # 處理 API Payload 或 DOM 解析
│   └── exporter.py         # 負責將資料格式化並輸出為 JSON 檔案
├── tests/                  # 測試區
│   ├── fixtures/           # 放置 Mock 用的靜態 JSON 或 HTML
│   └── test_parsers.py     # pytest-asyncio 單元測試
└── requirements.txt        # 專案依賴 (playwright, pytest, pytest-asyncio 等)
```

## 3. 模組介面 (Module Interfaces)
### 3.1 瀏覽器爬取模組 (`src/fetcher/`)
- **技術棧**: `playwright` (Async API)
- **職責**: 
  - 啟動 Headless Browser Context，設定擬真 User-Agent。
  - 導航至目標頁面並等待 Cloudflare Challenge 通過 (等待特定元件出現或超時)。
  - 透過 `page.on("response", ...)` 攔截網頁載入時的背景 API 封包。
- **錯誤處理**: 若遭遇無限驗證迴圈或逾時 (Timeout)，安全捕捉例外並將狀態標記為錯誤，不可引發整個爬蟲崩潰。

### 3.2 資料解析模組 (`src/parsers/`)
- **職責**: 解析從 Fetcher 攔截到的 API Payload 或是 DOM。
- **防呆機制**: 繼承 Phase 1，若 JSON Key 不存在或 DOM 變更，必須將該模組的 `status` 設為 `"error"`，嚴禁回傳預設值如 `null` 或 `0`，避免誤導下游 AI 交易策略。

### 3.3 輸出模組 (`src/exporter.py`)
- **職責**: 將彙整好的 Python Dictionary 轉譯為統一的 JSON 結構 (相容 Phase 1 Schema)，寫入 `wantgoo_market_data.json`。

## 4. 資料庫 Schema
本專案無關聯式資料庫。資料以本機 JSON 檔案落地，Schema 維持 Phase 1 定義不變，確保向下相容。
