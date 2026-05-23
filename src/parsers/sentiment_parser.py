from datetime import datetime, timezone, timedelta

def parse_sentiment(raw_data):
    if not raw_data or "sentiment" not in raw_data:
        return {"status": "error", "message": "Missing sentiment data"}
    
    data = raw_data["sentiment"]
    if data.get("net_position") is None:
        return {"status": "error", "message": "Missing net_position"}

    tz = timezone(timedelta(hours=8))
    return {
        "updated_at": datetime.now(tz).replace(microsecond=0).isoformat(),
        "status": "ok",
        "micro_tx_retail_ratio": {
            "net_position": data.get("net_position"),
            "ratio_pct": data.get("ratio_pct"),
            "daily_change": data.get("daily_change"),
        }
    }
