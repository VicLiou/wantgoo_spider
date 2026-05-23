# WantGoo Spider

> 自動化抓取玩股網盤後籌碼與市場廣度資訊。

---

## 🏛️ 專案架構 (Architecture & Directory Structure)
```text
.
├── src/
│   ├── main.py
│   ├── fetcher/
│   ├── parsers/
│   └── exporter.py
├── tests/
│   └── test_parsers.py
├── docs/
├── requirements.txt
└── README.md
```

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

## 🚀 啟動與使用 (Usage)
```bash
python src/main.py
```
執行後將在根目錄產生 `wantgoo_market_data.json`。

## 🧪 測試與驗證 (Testing & Quality Assurance)
```bash
pytest
```

## 🤖 維護聲明 (Maintainer Info)
- **開發者**: DDAD SDLC PG Bot
- **流水線**: 本專案由 SDLC 自動化開發流水線產出。
- **維護規範**: 後續開發者在新增功能或調整架構時，**必須**同步維護與更新此 README 文件。
