import json

def export_to_json(data, filepath="wantgoo_market_data.json"):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
