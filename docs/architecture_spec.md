# 系統架構規格 (System Architecture Specification) - Phase 3

## 專案名稱
wantgoo_spider

## 1. 系統架構總覽
本專案 (Phase 3) 為解決 Cloudflare 高階反爬蟲機制，針對核心爬取模組進行深度升級。在原有的 Playwright 非同步架構上，導入 `playwright-stealth` 隱形塗層，抹除無頭瀏覽器 (Headless Browser) 的自動化特徵。同時，加入隨機的擬人化動作 (如游標移動、捲動、隨機延遲)，確保能成功欺騙 Cloudflare 的行為分析並攔截目標資料。

## 2. 目錄結構 (Folder Structure)
```text
/home/ddad/projects/wantgoo_spider/
├── requirements.txt        # 專案依賴 (新增 playwright-stealth)
├── docs/                   # 系統與需求規格區
│   ├── PRD.md
│   ├── README.md           # 本次要求放置於 docs 目錄下
│   ├── architecture_spec.md
│   └── acceptance_criteria.md
├── src/                    # 應用程式原始碼
│   ├── main.py             # 程式進入點
│   ├── fetcher/            # Playwright 控制、Stealth 隱匿設定與擬人動作實作
│   ├── parsers/            # HTML/JSON 轉化與防呆機制
│   └── exporter.py         # JSON 檔案實體化輸出
└── tests/                  # 測試區
    ├── fixtures/           # Mock 假資料
    └── test_parsers.py     # 離線單元測試
```

## 3. 模組介面設計
### 3.1 隱匿爬取模組 (`src/fetcher/`)
- **技術棧**: `playwright`, `playwright-stealth`
- **職責**: 
  - 啟動 Browser Context，並於 Page 層級載入 stealth_sync / stealth_async。
  - 注入隨機且合理的 User-Agent 與 Viewport 大小。
  - 在發送核心 API 請求或解析 DOM 前，執行隨機延遲 (Sleep) 與頁面捲動 (Scroll)。
- **錯誤防護**: 若模擬失敗或超時，安全捕捉並回傳錯誤狀態予解析層，禁止引發全局崩潰。

### 3.2 資料解析與防護模組 (`src/parsers/`)
- **職責**: 解析取得的市場籌碼與廣度資料。
- **不妥協的防呆**: 嚴格保留 Phase 2 的 `status: error` 容錯機制。遇欄位短少，該子模組 `status` 標為 `"error"`，絕不輸出偽造之 `0` 或 `null`。
