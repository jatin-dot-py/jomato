#!/usr/bin/env python3
"""
Zomato Research Tool
"""
import sys
import argparse
import questionary
from src.utils import print_info, print_banner, print_error, clear_screen, console, get_access_token
from src._common import get_user_info


def show_menu():
    """Show interactive menu."""
    clear_screen()
    
    # Check auth
    access_token = get_access_token()
    user_name = None
    
    if access_token:
        with console.status("[bold cyan]Checking authentication...", spinner="dots"):
            user_info = get_user_info(access_token)
        if user_info.get("success"):
            user_name = user_info.get('data', {}).get('name', 'User')
    
    print_banner(user_name)
    
    choices = [
        "[1] Login",
        "[2] Logout",
        "[3] Food Rescue",
        "[0] Exit"
    ]
    
    selection = questionary.select(
        "Select:",
        choices=choices,
        style=questionary.Style([
            ('qmark', 'fg:#e94560 bold'),
            ('question', 'fg:#ffffff bold'),
            ('pointer', 'fg:#e94560 bold'),
            ('highlighted', 'fg:#ffffff bg:#e94560 bold'),
        ])
    ).ask()
    
    if not selection or "Exit" in selection:
        console.print("\n[dim]Goodbye![/dim]\n")
        sys.exit(0)
    
    if "Login" in selection:
        from src.auth.cli import run_login
        run_login()
    elif "Logout" in selection:
        from src.auth.cli import run_logout
        run_logout()
    elif "Food Rescue" in selection:
        from src.food_rescue.cli import run_food_rescue
        run_food_rescue()


def main():
    parser = argparse.ArgumentParser(
        description="Zomato - Unofficial API Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Login to Zomato')
    login_parser.add_argument('--phone', type=str, help='Phone number (without country code)')
    login_parser.add_argument('--otp-pref', type=str, choices=['sms', 'whatsapp', 'call'], 
                              help='OTP delivery method: sms, whatsapp, or call')
    
    # Logout command
    subparsers.add_parser('logout', help='Logout from Zomato')
    
    # Food rescue command
    subparsers.add_parser('food-rescue', help='Run Food Rescue listener')
    
    args = parser.parse_args()
    
    if args.command == 'login':
        from src.auth.cli import run_login
        run_login(phone=args.phone, otp_pref=getattr(args, 'otp_pref', None))
    elif args.command == 'logout':
        from src.auth.cli import run_logout
        run_logout()
    elif args.command == 'food-rescue':
        from src.food_rescue.cli import run_food_rescue
        run_food_rescue()
    else:
        show_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!][/bold yellow] Cancelled")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)
