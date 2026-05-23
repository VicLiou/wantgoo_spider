# WantGoo Spider - Phase 2 (Playwright Integration)

## 專案目標
解決 Phase 1 中 `requests` 被 Cloudflare 阻擋 (HTTP 403) 的問題。將抓取模組 (`fetcher`) 升級為 `playwright`。

## 功能需求
1. **升級 Fetcher**：將底層從 `requests` 換成 `playwright` (無頭瀏覽器模擬)。
2. **Cloudflare 繞過**：程式會啟動 browser context，等待 Cloudflare 驗證畫面通過後，再攔截 API 的 JSON 封包或解析 DOM。
3. **保留防呆機制**：Phase 1 的防呆容錯 (`status: error` 機制) 必須完整保留。
4. **測試架構更新**：調整 `pytest` 測試案例以配合 async/playwright 架構，繼續使用 Mock 機制，不輕易連線真實伺服器。
5. **環境配置更新**：更新 `requirements.txt` (加入 playwright) 與 `README.md` (說明 `playwright install`)。

## 分支與發布
- 分支名稱：`feature/phase2-playwright`
- PR 標題：`feat: 導入 Playwright 突破 Cloudflare 防護 (Phase 2)`
