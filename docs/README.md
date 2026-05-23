# WantGoo Spider (Phase 3)

玩股網 (WantGoo) 盤後籌碼與市場廣度自動化爬蟲專案 - Phase 3 終極破甲版。

## 核心升級說明
為對抗 Cloudflare 高階反爬蟲機制，本階段導入 `playwright-stealth` 與擬人化行為模式 (Human-like behavior)，包含抹除無頭瀏覽器特徵、隨機 Viewport、User-Agent 以及頁面載入後的捲動與等待動作。

## 系統需求
- Python 3.9+
- Playwright 與 Playwright-Stealth

## 快速啟動
```bash
# 1. 啟動環境與安裝依賴
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. 安裝瀏覽器引擎 (必需)
playwright install

# 3. 執行抓取程式
python src/main.py
```

## 測試規範 (嚴禁連線真實伺服器)
為了防止開發與 CI 流程遭目標伺服器封鎖，**測試環境下嚴禁發出真實 HTTP 請求**。
請使用 `pytest` 執行，所有的網路存取應被 Mock 並導向本地假資料：
```bash
pytest tests/
```

## 容錯機制
系統依然堅守嚴格的 `status: error` 防呆機制，當資料欄位無法解析時，決不預設回傳 0，避免汙染下游 AI 交易決策。
