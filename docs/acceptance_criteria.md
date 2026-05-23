# 驗收標準與邊界條件 (Acceptance Criteria & Edge Cases) - Phase 2

## 專案名稱
wantgoo_spider

## 1. 核心驗收標準 (Functional Acceptance Criteria)
1. **Cloudflare 突破**: 爬蟲能成功使用 `playwright` 通過 Cloudflare 驗證，不再發生 HTTP 403 阻擋而無法取得資料的問題。
2. **資料相容性**: 成功攔截或解析後，於專案根目錄產出的 `wantgoo_market_data.json` 檔案結構，必須 100% 吻合 Phase 1 定義 (包含 `sentiment_indicators`, `institutional_chips`, `market_breadth` 等欄位與 ISO 8601 時間戳)。

## 2. 測試規範 (Non-functional Acceptance Criteria - 強制要求)
1. **自動化測試更新**: 因引入非同步機制，單元測試需改用 `pytest-asyncio` 等非同步測試框架。
2. **強制 Mock 機制**: **嚴禁對真實的玩股網伺服器發出連線**。必須透過 Playwright 內建的路由攔截 (`page.route`) 或 Mock 套件，在測試執行時將請求導向 `tests/fixtures/` 內的假資料檔案。

## 3. 極端邊界條件 (Edge Cases for QA)
測試計畫與系統防護必須涵蓋以下情境 (Fail-Fast 與 Anti-Fragile 原則)：
1. **Cloudflare 驗證無限迴圈 (Timeout)**:
   - **情境**: 網站提高防護層級，導致無頭瀏覽器無法在合理時間內 (例如 30 秒) 通過 Challenge 驗證。
   - **預期行為**: `playwright` 需觸發 TimeoutError 並妥善捕捉。爬蟲應正常結束運行，並將所有模組或失敗模組的 `status` 標為 `"error"`。
2. **攔截目標 API 變更**:
   - **情境**: 目標網頁不再發送預期的 API (URL Path 改變) 或 HTML 結構大改。
   - **預期行為**: 抓取或解析失敗時，觸發防呆機制，該模組 `status` 標為 `"error"`，其餘未受影響的模組應正常輸出。
3. **無外網連線 (Network Down)**:
   - **情境**: 執行環境無網路。
   - **預期行為**: Playwright 啟動導航失敗，應優雅捕捉 DNS 或網路異常，產生 status 為 `"error"` 的空殼 JSON 並結束，避免引發 Unhandled Exception。
