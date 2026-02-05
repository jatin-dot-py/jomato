from typing import Literal
from curl_cffi import requests
from .authorize import url_authorize
from .sendotp import send_otp
from .submitotp import submit_otp
from .postconsent import post_consent
from .gettoken import get_token
import urllib
import base64
import hashlib
import secrets
import questionary

from src.utils import print_info, print_success, print_error, print_warning

def orchestrate_login(phone, otp_pref: Literal['sms', 'whatsapp', 'call']) -> dict | None:
    session = requests.Session(impersonate="chrome99_android",
        default_headers=False, akamai="1:65536;3:1000;4:6291456|15663105|0|m,a,s,p")

    code_verifier = secrets.token_urlsafe(32)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).decode().rstrip('=')

    print_info(f"Generated PKCE verifier and challenge")

    session.cookies.set('zxcv', code_verifier, domain='.zomato.com')
    session.cookies.set('cid', "5276d7f1-910b-4243-92ea-d27e758ad02b", domain='.zomato.com')
    session.cookies.set('rurl', "https://accounts.zomato.com/zoauth/callback", domain='.zomato.com')

    response = url_authorize(session, code_challenge)

    if not response.status_code == 200:
        print_error("URL authorize failed. Please try to login again.")
        return None

    login_challenge = urllib.parse.parse_qs(
            urllib.parse.urlparse(response.url).query
        )["login_challenge"][0]

    print_info(f"Sending OTP via {otp_pref.upper()}...")
    response = send_otp(session, phone, login_challenge, otp_pref)
    if not response.json()["status"]:
        print_error("Send OTP failed likely due to exhaustion. Please try again later.")
        return None

    otp = questionary.text("Enter OTP:", validate=lambda text: text.isdigit() and len(text) > 0).ask()
    if not otp:
        print_error("OTP is required")
        return None
    otp = int(otp)

    print_info("Verifying OTP...")
    response = submit_otp(session, phone, otp, login_challenge)
    if not response.status_code == 200:
        print_error("Submit OTP failed. Please try again later.")
        return None

    if not response.json()["status"]:
        print_error("Invalid OTP entered. Please run the login flow again.")
        return None

    redirect_url = response.json()["redirect_to"]

    response = session.get(redirect_url)

    consent_challenge = urllib.parse.parse_qs(
        urllib.parse.urlparse(response.url).query
    )['consent_challenge'][0]

    response = post_consent(session, consent_challenge)

    if not response.status_code == 200:
        print_error("Post consent failed. Please try again later.")
        return None

    if not response.json()["status"]:
        print_error("Invalid consent. Please run the login flow again.")
        return None

    redirect_url = response.json()["redirect_to"]

    response = session.get(redirect_url)

    parsed_url = urllib.parse.urlparse(response.url)
    qs = urllib.parse.parse_qs(parsed_url.query)

    code = qs.get('code', [None])[0]
    state = qs.get('state', [None])[0]
    scope = qs.get('scope', [None])[0]

    print_info("Exchanging authorization code for tokens...")
    response = get_token(session, code, scope, state, code_verifier)

    if response.status_code == 200:
        data = response.json()
        if data["status"]:
            token_data = data["token"]
            print_success("Authentication successful!")
            return {
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token", "")
            }
        else:
            print_error("Token exchange failed. Please try to login again.")
            return None
    else:
        print_error("Token exchange failed. Please try to login again.")
        return None
