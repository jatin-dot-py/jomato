"""Shared utilities for Zomato OSINT tool.

Provides:
- Token access (from .zomato config)
- CLI helpers (print_success, print_error, etc)
- Console and screen utilities
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key, unset_key
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.rule import Rule
from rich.padding import Padding
from rich import box
from rich.console import Group

# App config file
CONFIG_FILE = ".zomato"
load_dotenv(CONFIG_FILE)

console = Console()

# ============================================================================
# TOKEN MANAGEMENT
# ============================================================================

def get_access_token() -> str | None:
    """Get access token from .env"""
    return os.getenv("ZOMATO_ACCESS_TOKEN")

def get_refresh_token() -> str | None:
    """Get refresh token from .env"""
    return os.getenv("ZOMATO_REFRESH_TOKEN")

def save_tokens(access_token: str, refresh_token: str) -> None:
    """Save both tokens to .zomato config file."""
    if not os.path.exists(CONFIG_FILE):
        Path(CONFIG_FILE).touch()
    set_key(CONFIG_FILE, "ZOMATO_ACCESS_TOKEN", access_token)
    set_key(CONFIG_FILE, "ZOMATO_REFRESH_TOKEN", refresh_token)
    load_dotenv(CONFIG_FILE, override=True)

def clear_tokens() -> None:
    """Remove tokens from .zomato config file."""
    if os.path.exists(CONFIG_FILE):
        unset_key(CONFIG_FILE, "ZOMATO_ACCESS_TOKEN")
        unset_key(CONFIG_FILE, "ZOMATO_REFRESH_TOKEN")
        load_dotenv(CONFIG_FILE, override=True)

def has_tokens() -> bool:
    """Check if tokens exist."""
    return get_access_token() is not None

# ============================================================================
# CLI HELPERS
# ============================================================================

def print_success(message): 
    console.print(f"[bold green][✓][/bold green] {message}")

def print_info(message): 
    console.print(f"[bold cyan][+][/bold cyan] {message}")

def print_warning(message): 
    console.print(f"[bold yellow][!][/bold yellow] {message}")

def print_error(message): 
    console.print(f"[bold red][✗][/bold red] {message}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(user_name=None):
    """Display the main banner."""
    art = """
 ███████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗ ██████╗ 
 ╚══███╔╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝██╔═══██╗
   ███╔╝ ██║   ██║██╔████╔██║███████║   ██║   ██║   ██║
  ███╔╝  ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██║   ██║
 ███████╗╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╔╝
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ 
"""
    
    info_grid = Table.grid(padding=(0, 2))
    info_grid.add_column(style="cyan bold", justify="right")
    info_grid.add_column(style="white")
    
    if user_name:
        info_grid.add_row("Logged in as:", f"[green]{user_name}[/green]")
    
    dashboard_content = Group(
        Align.center(Text(art, style="bold red")),
        Align.center(Text("Research Tool", style="dim white")),
        Text(""),
        Padding(Align.center(info_grid), (1, 0, 0, 0)) if user_name else Text(""),
    )
    
    console.print(Panel(
        dashboard_content,
        border_style="red",
        width=70,
        box=box.ROUNDED
    ))
    console.print()
