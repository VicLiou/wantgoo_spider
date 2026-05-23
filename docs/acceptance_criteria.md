# 驗收標準與邊界條件 (Acceptance Criteria & Edge Cases) - Phase 3

## 專案名稱
wantgoo_spider

## 1. 核心驗收標準 (Functional Acceptance Criteria)
1. **隱形突破與擬人化行為**: 系統啟動時，必須確實載入 `playwright-stealth` 套件，並在抓取流程中包含隨機等待與捲動動作。最終成功抓取資料而無 403 阻擋。
2. **防呆容錯維持**: 即使目標網站版面大幅變更，系統不會 Crash，受影響的資料節點 `status` 將正確標示為 `"error"`。

## 2. 非功能驗收標準與測試 (Non-functional Acceptance Criteria)
1. **Mock 離線測試 (嚴格紅線)**: `pytest` 單元測試中，**絕對禁止**向真實伺服器連線。必須使用 Mock 手段 (如 `page.route` 或 `pytest-mock`) 攔截請求並讀取 `tests/fixtures/` 內的假資料。
2. **靜態分析檢查**: Python 程式碼須通過 Ruff 的 Linter 靜態語法檢查。

## 3. 極端邊界條件 (Edge Cases for QA)
1. **擬人化操作超時 (Action Timeout)**:
   - **情境**: 隨機捲動或延遲過程中，受到本機資源耗盡影響導致卡死。
   - **預期行為**: 設定全局與步驟 Timeout，捕捉逾時例外，中斷操作並輸出 `status: "error"` 確保流程結束。
2. **Stealth 失效被阻擋**:
   - **情境**: Cloudflare 再次升級特徵庫，即便使用 Stealth 依舊遇到 403 Forbidden。
   - **預期行為**: 網路請求攔截層偵測到 403 狀態碼時，應判斷抓取失敗，輸出錯誤 JSON 並優雅關閉瀏覽器實體。
