# WantGoo Spider Phase 3 (終極破甲) PRD

## 專案概述
- **專案名稱**：玩股網爬蟲系統 Phase 3
- **專案絕對路徑**：`/home/ddad/projects/wantgoo_spider`
- **目標**：解決 Phase 2 中 `playwright` 依舊被 Cloudflare 阻擋的問題。

## 功能需求 (Functional Requirements)
1. **導入 Stealth 隱形塗層**
   - 必須導入 `playwright-stealth` 以抹除 webdriver 的特徵。
   - 需要更新 `requirements.txt` 加入相關套件。
2. **擬人化行為 (Human-like Behavior)**
   - **隨機設定**：設定合理的 User-Agent 與 Viewport。
   - **模擬動作**：在頁面加載後、攔截 API 前，需加入隨機的等待 (Sleep) 與模擬捲動 (Scroll) 動作，以通過 Cloudflare 的行為分析。
3. **保留容錯機制**
   - 必須絕對保留原本的 `status: error` 防呆與容錯機制。

## 非功能需求與測試規範 (Non-Functional Requirements & QA)
- 測試必須維持 Mock 機制，**嚴禁在測試中連線真實伺服器**。
- 必須包含 pytest 單元測試與 Linter 檢查 (如 Ruff)。

## 部署與交付規範 (DevOps)
- 分支名稱：`feature/phase3-stealth`
- PR 標題：`feat: 導入 Stealth 隱形塗層與擬人化行為 (Phase 3)`
