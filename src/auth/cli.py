"""Auth CLI - Login and Logout commands."""
import sys
import questionary
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.utils import (
    console, get_access_token, get_refresh_token, save_tokens, clear_tokens, has_tokens,
    print_success, print_info, print_warning, print_error, print_banner, clear_screen
)
from src._common import get_user_info, logout


def run_login(phone=None, otp_pref=None):
    """Login to Zomato account.
    
    Args:
        phone: Phone number (optional, will prompt if not provided)
        otp_pref: OTP method - 'sms', 'whatsapp', or 'call' (optional)
    """
    from src.auth import orchestrate_login
    
    clear_screen()
    print_banner()
    
    # Check if already logged in
    if has_tokens():
        access_token = get_access_token()
        refresh_token = get_refresh_token()
        
        with console.status("[bold cyan]Checking current session...", spinner="dots"):
            user_info = get_user_info(access_token)
        
        if user_info.get("success"):
            user_name = user_info.get('data', {}).get('name', 'Unknown User')
            
            clear_screen()
            print_banner(user_name)
            
            console.print(Panel(
                f"You are already logged in as [green]{user_name}[/green]\n\n"
                f"Do you want to logout and login with a different account?",
                title="[bold yellow]Already Authenticated[/bold yellow]",
                border_style="yellow",
                box=box.ROUNDED
            ))
            console.print()
            
            should_logout = questionary.confirm("Logout and re-authenticate?", default=False).ask()
            
            if not should_logout:
                print_info("Keeping current session")
                return
            
            # Logout
            run_logout()
            console.print()
    
    print_info("Starting Zomato authentication flow")
    console.print()
    
    # Get phone
    if not phone:
        phone = questionary.text(
            "Enter your phone number (without country code, e.g., 9999999999):",
            validate=lambda text: len(text) > 5 or "Please enter a valid phone number"
        ).ask()
        if not phone:
            print_error("Phone number is required")
            sys.exit(1)
    
    # Get OTP method
    if not otp_pref:
        otp_method = questionary.select(
            "Select OTP delivery method:",
            choices=["WhatsApp", "SMS", "Call"],
            default="WhatsApp"
        ).ask()
        if not otp_method:
            print_error("OTP method is required")
            sys.exit(1)
        otp_pref = otp_method.lower()
    
    console.print()
    
    try:
        tokens = orchestrate_login(phone, otp_pref)
        
        if tokens and isinstance(tokens, dict):
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token", "")
            
            save_tokens(access_token, refresh_token)
            
            console.print()
            
            # Display tokens
            token_table = Table.grid(padding=(0, 2))
            token_table.add_column(style="cyan bold", justify="right", width=20)
            token_table.add_column(style="white")
            
            token_table.add_row("Access Token:", f"[green]{access_token[:50]}...[/green]")
            if refresh_token:
                token_table.add_row("Refresh Token:", f"[green]{refresh_token[:50]}...[/green]")
            token_table.add_row("", "")
            token_table.add_row("Saved to:", "[cyan].zomato[/cyan]")
            
            console.print(Panel(
                token_table,
                title="[bold green]✓ Login Successful[/bold green]",
                border_style="green",
                box=box.ROUNDED
            ))
            console.print()
        else:
            print_error("Login failed - no tokens received")
            sys.exit(1)
    except Exception as e:
        print_error(f"Login error: {e}")
        sys.exit(1)


def run_logout():
    """Logout from Zomato account."""
    if not has_tokens():
        print_warning("Not logged in")
        return False
    
    access_token = get_access_token()
    refresh_token = get_refresh_token()
    
    with console.status("[bold cyan]Logging out...", spinner="dots"):
        result = logout(access_token, refresh_token)
    
    if result.get("success"):
        clear_tokens()
        print_success("Logged out successfully")
        return True
    else:
        print_error(f"Logout failed: {result.get('error', 'Unknown error')}")
        print_warning("Tokens NOT cleared - you are still logged in")
        return False
