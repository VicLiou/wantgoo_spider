# WantGoo Spider

> 自動化抓取玩股網盤後籌碼與市場廣度資訊，內建 Phase 3 終極破甲 (Playwright Stealth + 真人行為模擬) 網路爬蟲系統。

---

## 🏛️ 專案架構 (Architecture & Directory Structure)

請根據實際產出的目錄結構描繪樹狀圖，讓接手開發者一目瞭然：

```text
.
├── src/                    # 核心程式碼
│   ├── main.py             # 程式進入點 (排程或單次執行)
│   ├── fetcher/            # 網路請求模組 (Playwright + Stealth)
│   │   └── api.py
│   ├── parsers/            # 資料解析與防呆模組
│   │   ├── sentiment_parser.py
│   │   ├── institutional_parser.py
│   │   └── breadth_parser.py
│   └── exporter.py         # JSON 檔案輸出模組
├── tests/                  # 測試案例
│   ├── test_fetcher.py     # fetcher 單元測試 (Mocking Playwright)
│   └── test_parsers.py     # 結構解析單元測試
├── docs/                   # 規格書與 PRD 文件
├── requirements.txt        # 依賴套件清單
└── README.md               # 專案指南 (本文件)
```

---

## ⚙️ 環境建置 (Prerequisites & Installation)

請提供最直接的快速啟動指令，確保任何人複製貼上皆可運行：

1. **建立並啟動虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **安裝依賴套件與瀏覽器核心**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

---

## 🚀 啟動與使用 (Usage)

列出啟動服務的指令以及預期的結果。

**執行爬蟲程式**：
```bash
python src/main.py
```

**預期結果**：
執行完畢後，將於專案根目錄產生 `wantgoo_market_data.json` 檔案，內容包含結構化之盤後資訊。系統已內建隨機 User-Agent、Viewport 與捲動行為來繞過 Cloudflare：
```json
{
  "global_timestamp": "2026-05-23T22:50:00+08:00",
  "data": {
    "sentiment_indicators": {...},
    "institutional_chips": {...},
    "market_breadth": {...}
  }
}
```

---

## 🧪 測試與驗證 (Testing & Quality Assurance)

本專案嚴格遵守測試驅動與代碼品質規範：

**執行單元測試 (Pytest)**：
```bash
pytest
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
