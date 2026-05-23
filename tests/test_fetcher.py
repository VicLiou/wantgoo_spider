import sys
import os
from unittest.mock import MagicMock, patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fetcher.api import fetch_wantgoo_data

@patch('src.fetcher.api.stealth')
@patch('src.fetcher.api.sync_playwright')
def test_fetch_wantgoo_data_success(mock_sync_playwright, mock_stealth):
    mock_data = {
        "sentiment": {"net_position": 2500, "ratio_pct": 15.2, "daily_change": 500},
        "institutional": {"foreign_net_position": -5200, "foreign_daily_change": -1200, "top10_specific_net_position": 1200, "top10_daily_change": 300},
        "breadth": {"advancing_issues": 650, "declining_issues": 230, "bullish_alignment_pct": 45.5, "bearish_alignment_pct": 30.2}
    }
    
    # Setup mock playwright context
    mock_playwright = MagicMock()
    mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
    
    mock_browser = MagicMock()
    mock_playwright.chromium.launch.return_value = mock_browser
    
    mock_context = MagicMock()
    mock_browser.new_context.return_value = mock_context
    
    mock_page = MagicMock()
    mock_context.new_page.return_value = mock_page
    
    # Simulate the response handler
    def simulate_goto(*args, **kwargs):
        # Find the registered event handler for 'response'
        for call in mock_page.on.call_args_list:
            if call[0][0] == 'response':
                handler = call[0][1]
                mock_response = MagicMock()
                mock_response.url = "https://www.wantgoo.com/api/market/data"
                mock_response.status = 200
                mock_response.json.return_value = mock_data
                handler(mock_response)
    
    mock_page.goto.side_effect = simulate_goto
    
    result = fetch_wantgoo_data()
    assert result == mock_data

@patch('src.fetcher.api.stealth')
@patch('src.fetcher.api.sync_playwright')
def test_fetch_wantgoo_data_failure(mock_sync_playwright, mock_stealth):
    mock_playwright = MagicMock()
    mock_sync_playwright.return_value.__enter__.return_value = mock_playwright
    mock_playwright.chromium.launch.side_effect = Exception("Browser launch failed")
    
    result = fetch_wantgoo_data()
    assert result is None
