import requests

try:
    from src.get_user_locations import get_user_locations
except ImportError:
    from get_user_locations import get_user_locations

BASE_URL = "https://api.zomato.com/gw/tabbed-home"

HEADERS = {
    "Accept": "image/webp",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "X-Zomato-API-Key": "7749b19667964b87a3efc739e254ada2",
    "X-Zomato-App-Version": "931",
    "X-Zomato-App-Version-Code": "1710019310",
    "X-Zomato-Client-Id": "5276d7f1-910b-4243-92ea-d27e758ad02b",
    "X-Zomato-UUID": "b2691abb-5aac-48a5-9f0e-750349080dcb"
}

def extract_food_rescue_channels(config: dict) -> list:
    """Extract food rescue subscription channels and MQTT credentials."""
    channels = []
    
    for channel in config.get("subscription_channels", []):
        if channel.get("type") == "food_rescue":
            client = channel.get("client", {})
            channels.append({
                "channel_name": channel.get("name", [None])[0],
                "qos": channel.get("qos"),
                "valid_until": channel.get("time"),
                "mqtt_username": client.get("username"),
                "mqtt_password": client.get("password"),
                "mqtt_keepalive": client.get("keepalive"),
            })
    
    return channels


def get_food_rescue_config(cell_id: str, address_id: int, access_token: str = None) -> dict:
    """Fetch food rescue configuration for a given location."""
    params = {
        "cell_id": cell_id,
        "address_id": str(address_id),
    }
    
    current_headers = HEADERS.copy()
    if access_token:
        current_headers["X-Zomato-Access-Token"] = access_token
        
    response = requests.get(BASE_URL, headers=current_headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data

