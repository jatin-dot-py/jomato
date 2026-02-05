"""Common API calls used across all modules."""
import requests

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


def get_user_info(access_token: str) -> dict:
    """Get current user info from Zomato API."""
    url = "https://api.zomato.com/gw/user/info"
    headers = {**HEADERS, "X-Zomato-Access-Token": access_token}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def get_user_locations(access_token: str) -> list:
    """Get user's saved locations."""
    url = "https://api.zomato.com/gw/user/location/selection"
    
    payload = {
        "android_country": "",
        "location_permissions": {
            "device_location_on": False,
            "location_permission_available": False,
            "precise_location_permission_available": False
        },
        "current_app_address_id": None,
        "incremental_call": False,
        "source": "delivery_home",
        "lang": "en",
        "android_language": "en",
        "postback_params": "{}",
        "recent_locations": [],
        "city_id": "1"
    }
    
    headers = {
        **HEADERS,
        "Content-Type": "application/json; charset=UTF-8",
        "X-Zomato-Access-Token": access_token
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    locations = []
    for result in data.get("response", {}).get("results", []):
        snippet = result.get("location_address_snippet")
        if not snippet:
            continue
        
        click_action = snippet.get("click_action", {})
        update_result = click_action.get("update_location_result", {})
        address = update_result.get("address", {})
        place = address.get("place", {})
        
        if not address.get("id"):
            continue
        
        locations.append({
            "address_id": address.get("id"),
            "cell_id": place.get("cell_id"),
            "name": snippet.get("title", {}).get("text") or address.get("alias"),
            "full_address": snippet.get("subtitle", {}).get("text") or address.get("display_subtitle"),
        })
    
    return locations


def logout(access_token: str, refresh_token: str) -> dict:
    """Sign out from Zomato account.
    
    Returns:
        dict with 'success' bool and optional 'error' message
    """
    url = "https://accounts.zomato.com/signout"
    
    headers = {
        "Accept": "image/webp",
        "Accept-Encoding": "br, gzip",
        "Connection": "Keep-Alive",
        "Content-Length": "0",
        "Host": "accounts.zomato.com",
        "is-akamai-video-optimisation-enabled": "1",
        "pragma": "akamai-x-get-request-id,akamai-x-cache-on, akamai-x-check-cacheable",
        "User-Agent": "&source=android_market&version=10&device_manufacturer=Google&device_brand=google&device_model=Android+SDK+built+for+x86_64&api_version=931&app_version=v19.3.1",
        "USER-BUCKET": "100",
        "USER-HIGH-PRIORITY": "4",
        "X-Access-UUID": "627d3590-a3aa-4230-a0eb-132994eba61b",
        "X-Accessibility-Dynamic-Text-Scale-Factor": "1.0",
        "X-Accessibility-Voice-Over-Enabled": "0",
        "X-Android-Id": "29435aa6a6755a97",
        "X-APP-APPEARANCE": "LIGHT",
        "X-App-Language": "&lang=en&android_language=en&android_country=",
        "X-App-Session-Id": "1da5f0ce-0982-47d9-8319-59fbdbd7172b",
        "X-APP-THEME": "default",
        "X-Appsflyer-UID": "1770243703663-5635532006973144283",
        "X-BLINKIT-INSTALLED": "false",
        "X-Bluetooth-On": "false",
        "X-City-Id": "1",
        "X-Client-Id": "zomato_android_v2",
        "X-Device-Height": "2208",
        "X-Device-Language": "en",
        "X-Device-Pixel-Ratio": "2.75",
        "X-Device-Width": "1080",
        "X-DISTRICT-INSTALLED": "false",
        "X-FIREBASE-INSTANCE-ID": "3bc79ef61af45c349bef251f2de8d858",
        "X-Installer-Package-Name": "cm.aptoide.pt",
        "X-Jumbo-Session-Id": "5375d9d1-fdb3-47da-b675-009a67336e321770243704",
        "X-Network-Type": "mobile_UNKNOWN",
        "X-O2-City-Id": "1",
        "x-perf-class": "PERFORMANCE_AVERAGE",
        "X-Present-Horizontal-Accuracy": "-1",
        "X-Present-Lat": "0.0",
        "X-Present-Long": "0.0",
        "X-Request-Id": "2b5a2e0a-bbe7-4963-b5ee-7624a356e342",
        "X-RIDER-INSTALLED": "false",
        "X-SYSTEM-APPEARANCE": "UNSPECIFIED",
        "X-User-Defined-Lat": "28.6109026",
        "X-User-Defined-Long": "77.1149472",
        "X-VPN-Active": "1",
        "X-Zomato-Access-Token": access_token,
        "X-Zomato-API-Key": "7749b19667964b87a3efc739e254ada2",
        "X-Zomato-App-Version": "931",
        "X-Zomato-App-Version-Code": "1710019310",
        "X-Zomato-Client-Id": "5276d7f1-910b-4243-92ea-d27e758ad02b",
        "X-Zomato-Is-Metric": "true",
        "X-Zomato-Refresh-Token": refresh_token,
        "X-Zomato-UUID": "b2691abb-5aac-48a5-9f0e-750349080dcb"
    }
    
    # Cookies as per the spec
    cookies = {
        "zxcv": "",
        "rurl": "https://accounts.zomato.com/zoauth/callback",
        "cid": "5276d7f1-910b-4243-92ea-d27e758ad02b"
    }
    
    try:
        response = requests.post(url, headers=headers, cookies=cookies)
        data = response.json()
        # API returns "status" not "success"
        return {"success": data.get("status", False), "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}
