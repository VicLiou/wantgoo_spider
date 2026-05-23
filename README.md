# WantGoo Spider

> 玩股網 (WantGoo) 盤後籌碼與市場廣度自動化爬蟲專案，專為下游 AI 交易代理人提供結構化市場指標資料 (Phase 2: Playwright 升級版)。

---

## 🏛️ 專案架構 (Architecture & Directory Structure)


```text
.
├── src/                # 核心程式碼 (包含 fetcher, parsers, exporter)
│   ├── main.py
│   ├── fetcher/
│   └── parsers/
├── tests/              # 測試案例 (Mock 機制)
│   ├── test_fetcher.py
│   └── test_parsers.py
├── docs/               # 規格書與 QA 報告
├── requirements.txt    # 依賴套件清單 (含 playwright)
└── README.md           # 專案指南 (本文件)
```

---

## ⚙️ 環境建置 (Prerequisites & Installation)


1. **建立並啟動虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

3. **安裝 Playwright 瀏覽器引擎 (必須執行)**
   ```bash
   playwright install
   ```

---

## 🚀 啟動與使用 (Usage)

**啟動服務**：
```bash
python src/main.py
```

**預期結果**：
執行完畢後，將於專案根目錄產出符合投資蝦需求規格之 `wantgoo_market_data.json` 檔案。

---

## 🧪 測試與驗證 (Testing & Quality Assurance)

本專案嚴格遵守測試驅動與代碼品質規範，單元測試嚴禁發出真實 HTTP 請求：

**執行非同步單元測試 (Pytest)**：
```bash
pytest tests/
```

**執行靜態檢查 (Ruff)**：
```bash
ruff check .
```

---

## 🤖 維護聲明 (Maintainer Info)
- **開發者**: DDAD SDLC PG Bot
- **流水線**: 本專案由 SDLC 自動化開發流水線產出。
- **維護規範**: 後續開發者在新增功能或調整架構時，**必須**同步維護與更新此 README 文件。
