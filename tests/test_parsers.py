import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.sentiment_parser import parse_sentiment
from src.parsers.institutional_parser import parse_institutional
from src.parsers.breadth_parser import parse_breadth

def test_parse_sentiment_success():
    raw = {"sentiment": {"net_position": 100, "ratio_pct": 5.0, "daily_change": 10}}
    res = parse_sentiment(raw)
    assert res["status"] == "ok"
    assert res["micro_tx_retail_ratio"]["net_position"] == 100

def test_parse_sentiment_error():
    raw = {"sentiment": {"ratio_pct": 5.0}} # missing net_position
    res = parse_sentiment(raw)
    assert res["status"] == "error"

def test_parse_institutional_success():
    raw = {"institutional": {"foreign_net_position": -500, "foreign_daily_change": -100, "top10_specific_net_position": 200, "top10_daily_change": 50}}
    res = parse_institutional(raw)
    assert res["status"] == "ok"
    assert res["foreign_tx_net_position"] == -500

def test_parse_institutional_error():
    raw = {} # missing completely
    res = parse_institutional(raw)
    assert res["status"] == "error"

def test_parse_breadth_success():
    raw = {"breadth": {"advancing_issues": 300, "declining_issues": 100, "bullish_alignment_pct": 50.0, "bearish_alignment_pct": 20.0}}
    res = parse_breadth(raw)
    assert res["status"] == "ok"
    assert res["advancing_issues"] == 300

def test_parse_breadth_error():
    raw = {"breadth": {"declining_issues": 100}} # missing advancing
    res = parse_breadth(raw)
    assert res["status"] == "error"
