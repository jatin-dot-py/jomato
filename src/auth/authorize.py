import secrets
import string

def generate_state_string(length=32):
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def url_authorize(session, code_challenge):
    url = "https://accounts.zomato.com/oauth2/auth"

    params = {
        "urlAuthorize": "https://accounts.zomato.com/oauth/auth",
        "approval_prompt": "auto",
        "scope": "offline openid",
        "response_type": "code",
        "code_challenge_method": "S256",
        "redirect_uri": "https://accounts.zomato.com/zoauth/callback",
        "state": generate_state_string(),
        "client_id": "5276d7f1-910b-4243-92ea-d27e758ad02b",
        "code_challenge": code_challenge,
    }

    headers = {
        "Accept": "image/webp",
        "Accept-Encoding": "br, gzip",
        "Connection": "Keep-Alive",
        "Host": "accounts.zomato.com",
        "is-akamai-video-optimisation-enabled": "0",
        "pragma": "akamai-x-get-request-id,akamai-x-cache-on, akamai-x-check-cacheable",
        "User-Agent": "&source=android_market&version=10&device_manufacturer=Google&device_brand=google&device_model=Android+SDK+built+for+x86_64&api_version=931&app_version=v19.3.1",
        "USER-BUCKET": "0",
        "USER-HIGH-PRIORITY": "0",
        "X-Access-UUID": "71783d00-13fc-4e81-9ba6-9428f2c6c75c",
        "X-Accessibility-Dynamic-Text-Scale-Factor": "1.0",
        "X-Accessibility-Voice-Over-Enabled": "0",
        "X-Android-Id": "29435aa6a6755a97",
        "X-APP-APPEARANCE": "LIGHT",
        "X-App-Language": "&lang=en&android_language=en&android_country=",
        "X-App-Session-Id": "b287175a-035e-4346-b8fb-0b19c4892cea",
        "X-APP-THEME": "default",
        "X-Appsflyer-UID": "1770210645057-4891034784193940182",
        "X-BLINKIT-INSTALLED": "false",
        "X-Bluetooth-On": "false",
        "X-City-Id": "-1",
        "X-Client-Id": "zomato_android_v2",
        "X-Device-Height": "2208",
        "X-Device-Language": "en",
        "X-Device-Pixel-Ratio": "2.75",
        "X-Device-Width": "1080",
        "X-DISTRICT-INSTALLED": "false",
        "X-FIREBASE-INSTANCE-ID": "3bc79ef61af45c349bef251f2de8d858",
        "X-Installer-Package-Name": "cm.aptoide.pt",
        "X-Jumbo-Session-Id": "e26bfcdb-8b7f-462d-a388-d49f6652c0e71770231893",
        "X-Network-Type": "mobile_UNKNOWN",
        "X-O2-City-Id": "-1",
        "x-perf-class": "PERFORMANCE_AVERAGE",
        "X-Present-Horizontal-Accuracy": "-1",
        "X-Present-Lat": "0.0",
        "X-Present-Long": "0.0",
        "X-Request-Id": "69e0492f-48b1-40f2-850c-18f12d92991c",
        "X-RIDER-INSTALLED": "false",
        "X-SYSTEM-APPEARANCE": "UNSPECIFIED",
        "X-User-Defined-Lat": "0.0",
        "X-User-Defined-Long": "0.0",
        "X-VPN-Active": "1",
        "X-Zomato-API-Key": "7749b19667964b87a3efc739e254ada2",
        "X-Zomato-App-Version": "931",
        "X-Zomato-App-Version-Code": "1710019310",
        "X-Zomato-Client-Id": "5276d7f1-910b-4243-92ea-d27e758ad02b",
        "X-Zomato-UUID": "b2691abb-5aac-48a5-9f0e-750349080dcb"
    }
    response = session.get(url, params=params, headers=headers)
    return response