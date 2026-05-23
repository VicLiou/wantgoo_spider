import random
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
]

VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1440, "height": 900},
    {"width": 1366, "height": 768},
    {"width": 1536, "height": 864}
]

def fetch_wantgoo_data():
    """
    使用 Playwright 啟動 Browser Context，並搭配 playwright-stealth 進行破甲。
    包含隨機 User-Agent、Viewport，以及模擬真人行為的隨機捲動與等待。
    攔截 API 回傳的 JSON 數據。若失敗則回傳 None 觸發防呆機制。
    """
    raw_data = None
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # 1. 隨機設定合理的 User-Agent 和 Viewport
            ua = random.choice(USER_AGENTS)
            vp = random.choice(VIEWPORTS)
            
            context = browser.new_context(
                user_agent=ua,
                viewport=vp
            )
            page = context.new_page()

            # 2. 必須使用 playwright-stealth 抹除 webdriver 特徵
            stealth(page)

            def handle_response(response):
                nonlocal raw_data
                if "api/market/data" in response.url and response.status == 200:
                    try:
                        raw_data = response.json()
                    except Exception:
                        pass

            page.on("response", handle_response)

            # 導向目標頁面
            page.goto("https://www.wantgoo.com/market", wait_until="domcontentloaded", timeout=30000)

            # 3. 在頁面加載後、攔截 API 前，加入隨機的等待 (Sleep) 與捲動 (Scroll) 動作
            time.sleep(random.uniform(1.0, 2.5))
            page.mouse.wheel(0, random.randint(300, 700))
            time.sleep(random.uniform(0.5, 1.5))
            page.mouse.wheel(0, random.randint(200, 500))

            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                pass # 即使發生 timeout，若已經攔截到資料仍繼續往下執行

            browser.close()
            return raw_data

    except Exception:
        # 4. 絕對保留原本的 status: error 防呆容錯機制
        return None
