import os
import sys
from datetime import datetime, timezone, timedelta

# Add src to python path for local execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fetcher.api import fetch_wantgoo_data
from src.parsers.sentiment_parser import parse_sentiment
from src.parsers.institutional_parser import parse_institutional
from src.parsers.breadth_parser import parse_breadth
from src.exporter import export_to_json

def main():
    raw_data = fetch_wantgoo_data()
    
    sentiment_data = parse_sentiment(raw_data)
    institutional_data = parse_institutional(raw_data)
    breadth_data = parse_breadth(raw_data)
    
    tz = timezone(timedelta(hours=8))
    final_output = {
        "global_timestamp": datetime.now(tz).replace(microsecond=0).isoformat(),
        "data": {
            "sentiment_indicators": sentiment_data,
            "institutional_chips": institutional_data,
            "market_breadth": breadth_data
        }
    }
    
    export_to_json(final_output, "wantgoo_market_data.json")
    print("Data exported to wantgoo_market_data.json")

if __name__ == "__main__":
    main()
