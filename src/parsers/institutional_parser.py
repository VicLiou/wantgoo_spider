from datetime import datetime, timezone, timedelta

def parse_institutional(raw_data):
    if not raw_data or "institutional" not in raw_data:
        return {"status": "error", "message": "Missing institutional data"}
    
    data = raw_data["institutional"]
    if data.get("foreign_net_position") is None:
        return {"status": "error", "message": "Missing foreign_net_position"}

    tz = timezone(timedelta(hours=8))
    return {
        "updated_at": datetime.now(tz).replace(microsecond=0).isoformat(),
        "status": "ok",
        "foreign_tx_net_position": data.get("foreign_net_position"),
        "foreign_daily_change": data.get("foreign_daily_change"),
        "top10_specific_net_position": data.get("top10_specific_net_position"),
        "top10_daily_change": data.get("top10_daily_change")
    }
