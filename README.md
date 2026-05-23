# WantGoo Spider

玩股網 (WantGoo) 盤後籌碼與市場廣度自動化爬蟲專案。本服務專為下游 AI 交易代理人提供結構化市場指標資料。
於 **Phase 2** 中，系統已升級採用 `playwright` 以繞過 Cloudflare HTTP 403 阻擋。

## 系統需求
- Python 3.9+
- 採用 `playwright` 作為底層爬蟲引擎 (支援 Async)
- JSON 資料匯出

## 開發與安裝
```bash
# 1. 建立並啟動虛擬環境 (建議)
python3 -m venv venv
source venv/bin/activate

# 2. 安裝依賴套件
pip install -r requirements.txt

# 3. 安裝 Playwright 瀏覽器引擎 (必須執行)
playwright install
```

## 執行方式
```bash
python src/main.py
```
執行完畢後，將於專案根目錄產出相容於 Phase 1 結構的 `wantgoo_market_data.json`。

## 測試規範 (非常重要)
為避免觸發目標網站的反爬蟲機制及浪費頻寬，**單元測試嚴禁發出真實 HTTP 請求**。
QA 團隊與開發者必須使用 Playwright 的 `page.route` 或其他 Mock 機制，將網路請求導向 `tests/fixtures/` 的假資料：
```bash
# 執行非同步單元測試
pytest tests/
```

## 核心機制與防呆 (Phase 2)
1. 自動等待 Cloudflare 驗證完成。
2. 若遇到網頁改版、API 變更或 Timeout 導致欄位遺失，輸出結果會精準將該模組標示為 `status: "error"`，嚴格禁止自動將遺失數值補零。
