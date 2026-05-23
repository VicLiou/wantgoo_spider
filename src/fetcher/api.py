import requests

def fetch_wantgoo_data():
    try:
        response = requests.get("https://www.wantgoo.com/api/market/data", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        # 發生錯誤時記錄並回傳 None，確保不崩潰
        return None
