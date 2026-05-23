from datetime import datetime, timezone, timedelta

def parse_breadth(raw_data):
    if not raw_data or "breadth" not in raw_data:
        return {"status": "error", "message": "Missing breadth data"}
    
    data = raw_data["breadth"]
    if data.get("advancing_issues") is None:
        return {"status": "error", "message": "Missing advancing_issues"}

    tz = timezone(timedelta(hours=8))
    return {
        "updated_at": datetime.now(tz).replace(microsecond=0).isoformat(),
        "status": "ok",
        "advancing_issues": data.get("advancing_issues"),
        "declining_issues": data.get("declining_issues"),
        "bullish_alignment_pct": data.get("bullish_alignment_pct"),
        "bearish_alignment_pct": data.get("bearish_alignment_pct")
    }
