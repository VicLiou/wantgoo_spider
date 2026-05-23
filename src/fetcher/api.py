from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def fetch_wantgoo_data():
    """
    使用 Playwright 啟動 Browser Context，等待 Cloudflare 驗證通過後，
    攔截 API 回傳的 JSON 數據。若失敗則回傳 None 觸發防呆機制。
    """
    raw_data = None
    
    try:
        with sync_playwright() as p:
            # 啟動 Chromium
            browser = p.chromium.launch(headless=True)
            # 建立 Context 並設置常用 User-Agent 增加通過 Cloudflare 的機率
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            def handle_response(response):
                nonlocal raw_data
                # 攔截包含資料的 API endpoint (URL依實際情況微調)
                if "api/market/data" in response.url and response.status == 200:
                    try:
                        raw_data = response.json()
                    except Exception:
                        pass

            # 綁定 Response 攔截器
            page.on("response", handle_response)

            # 導向目標頁面
            page.goto("https://www.wantgoo.com/market", wait_until="domcontentloaded", timeout=30000)

            # 靜候一段時間等待 Cloudflare 驗證畫面通過與資料加載
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                pass # 即使發生 timeout，若已經攔截到資料仍繼續往下執行

            browser.close()
            
            # 回傳攔截到的 JSON 結構，若未抓到則會是 None
            return raw_data

    except Exception:
        # 發生任何不可預期錯誤 (例如瀏覽器啟動失敗) 皆回傳 None
        # 讓下層 parsers 啟動防呆容錯機制 (status: error)
        return None
