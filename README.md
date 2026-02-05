# Jomato 🍅

Unofficial OSINT, Intelligence, and Utility Toolkit for Zomato.

Jomato is a reverse-engineered Python wrapper for the Zomato API. It provides a robust authentication bundle, OSINT capabilities for geospatial analysis, and utility features for power users.

Designed for security researchers, data analysts, and developers.

## ⚠️ Legal Disclaimer

This tool is **NOT** affiliated with, endorsed by, or connected to Zomato or Eternal Ltd.

This software is provided for educational and research purposes only. The author assumes no liability for any misuse of this tool or for any damages caused by its use. Users are responsible for ensuring their activities comply with Zomato's Terms of Service and applicable local laws.

## Installation

```bash
git clone https://github.com/jatin-dot-py/jomato.git
cd jomato
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
python zomato.py
```

### Commands

**Login:**
```bash
python zomato.py login
```

Or with arguments:
```bash
python zomato.py login --phone 9999999999 --otp-pref sms
```

OTP preferences: `sms`, `whatsapp`, `call`

**Logout:**
```bash
python zomato.py logout
```

**Help:**
```bash
python zomato.py --help
python zomato.py login --help
```

## Configuration

Tokens are stored in `.zomato` file (gitignored).
