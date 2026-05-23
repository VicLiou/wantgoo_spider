# 驗收標準與邊界條件 (Acceptance Criteria & Edge Cases)

## 專案名稱
wantgoo_spider

## 1. 核心驗收標準 (Functional Acceptance Criteria)
1. **資料爬取與 JSON 產出**: 程式執行完成後，必須於專案根目錄產生 (或覆寫) `wantgoo_market_data.json` 檔案。
2. **Schema 一致性**: 輸出的 JSON 結構必須 100% 吻合 PRD 中第 3 節定義之格式，包含三個子模組：`sentiment_indicators`, `institutional_chips`, `market_breadth`。
3. **時間戳記格式**: 所有 `updated_at` 與 `global_timestamp` 必須具備正確的 ISO 8601 時區資訊 (如 `+08:00`)。

## 2. 測試規範 (Non-functional Acceptance Criteria - 強制要求)
1. **強制 Mock 機制**: QA 或自動化測試在執行 `pytest` 時，**嚴禁對玩股網正式機 (Production) 發出真實的 HTTP 請求**。
2. **測試實作方式**: 必須使用 `unittest.mock`, `pytest-mock`，或者 `responses` / `requests-mock` 套件攔截 HTTP 呼叫，並由 `tests/fixtures/` 提供預先下載好的靜態假網頁或假 JSON 回應檔。

## 3. 極端邊界條件 (Edge Cases for QA)
測試計畫與系統防護必須涵蓋以下情境 (Fail-Fast 與 Anti-Fragile 原則)：
1. **網頁結構變動 / API 欄位消失**:
   - **情境**: 玩股網改版，導致 BeautifulSoup 找不到特定的 div/table，或 API JSON 缺少指定 key。
   - **預期行為**: 該子模組的 `status` 必須精準標記為 `"error"`，其數值欄位不可自動補 `0` 也不可引發全局 Crash。其餘未受影響的子模組應正常解析。
2. **連線逾時 (Timeout) 或 阻擋 (HTTP 403 / 429)**:
   - **情境**: 網路斷線或被目標伺服器限流 (Rate Limiting)。
   - **預期行為**: `requests` 層必須捕捉 Timeout 異常，整個資料區塊 `status` 寫入 `"error"` 並優雅結束，不得出現 Unhandled Exception 導致 CI 噴錯。
3. **資料型態異常**:
   - **情境**: 預期抓取整數部位量，但抓到空字串 `""` 或 `"-"` 或非數值字元。
   - **預期行為**: Parser 轉型失敗時，該模組 `status` 標為 `"error"`，嚴格禁止將空字串當作 0 來計算，以防止引發嚴重交易邏輯錯誤。
