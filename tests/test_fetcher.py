import sys
import os
import responses
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fetcher.api import fetch_wantgoo_data

@responses.activate
def test_fetch_wantgoo_data_success():
    mock_data = {
        "sentiment": {"net_position": 2500, "ratio_pct": 15.2, "daily_change": 500},
        "institutional": {"foreign_net_position": -5200, "foreign_daily_change": -1200, "top10_specific_net_position": 1200, "top10_daily_change": 300},
        "breadth": {"advancing_issues": 650, "declining_issues": 230, "bullish_alignment_pct": 45.5, "bearish_alignment_pct": 30.2}
    }
    responses.add(
        responses.GET,
        "https://www.wantgoo.com/api/market/data",
        json=mock_data,
        status=200
    )

    result = fetch_wantgoo_data()
    assert result == mock_data

@responses.activate
def test_fetch_wantgoo_data_failure():
    responses.add(
        responses.GET,
        "https://www.wantgoo.com/api/market/data",
        status=500
    )

    result = fetch_wantgoo_data()
    assert result is None

@responses.activate
def test_fetch_wantgoo_data_timeout():
    import requests
    responses.add(
        responses.GET,
        "https://www.wantgoo.com/api/market/data",
        body=requests.exceptions.Timeout()
    )
    result = fetch_wantgoo_data()
    assert result is None
