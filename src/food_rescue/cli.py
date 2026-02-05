"""Food Rescue CLI."""
import sys
import questionary
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.utils import (
    console, get_access_token, 
    print_success, print_info, print_warning, print_error,
    print_banner, clear_screen
)
from src._common import get_user_info, get_user_locations


def run_food_rescue():
    """Run Food Rescue listener."""
    from src.food_rescue.get_food_rescue_conf import get_food_rescue_config, extract_food_rescue_channels
    
    clear_screen()
    print_banner()
    
    access_token = get_access_token()
    
    if not access_token:
        print_error("Not logged in. Run: python zomato.py login")
        sys.exit(1)
    
    with console.status("[bold cyan]Verifying session...", spinner="dots"):
        user_info = get_user_info(access_token)
    
    if not user_info.get("success"):
        print_error("Authentication failed. Please login again.")
        sys.exit(1)
    
    user_name = user_info.get('data', {}).get('name', 'User')
    clear_screen()
    print_banner(user_name)
    
    print_info("Fetching your saved locations...")
    try:
        locations = get_user_locations(access_token)
    except Exception as e:
        print_error(f"Error fetching locations: {e}")
        sys.exit(1)
    
    if not locations:
        print_warning("No saved locations found")
        sys.exit(1)
    
    print_success(f"Found {len(locations)} location(s)")
    console.print()
    
    location_choices = [f"{loc['name']} ({loc['full_address']})" for loc in locations]
    
    selected = questionary.select(
        "Select monitoring location:",
        choices=location_choices,
        style=questionary.Style([
            ('qmark', 'fg:#e94560 bold'),
            ('pointer', 'fg:#e94560 bold'),
            ('highlighted', 'fg:#ffffff bg:#e94560 bold'),
        ])
    ).ask()
    
    if not selected:
        print_warning("Cancelled")
        sys.exit(0)
    
    selected_loc = next(l for l in locations if f"{l['name']} ({l['full_address']})" == selected)
    
    console.print()
    
    # Location panel
    loc_table = Table.grid(padding=(0, 2))
    loc_table.add_column(style="cyan bold", justify="right")
    loc_table.add_column(style="white")
    loc_table.add_row("Location:", f"[green]{selected_loc['name']}[/green]")
    loc_table.add_row("Address:", f"[dim]{selected_loc['full_address']}[/dim]")
    
    console.print(Panel(loc_table, title="[bold green]Active Location[/bold green]", border_style="green", box=box.ROUNDED))
    console.print()
    
    print_info("Fetching Food Rescue configuration...")
    try:
        config = get_food_rescue_config(selected_loc['cell_id'], selected_loc['address_id'], access_token)
        channels = extract_food_rescue_channels(config)
    except Exception as e:
        print_error(f"Error: {e}")
        sys.exit(1)
    
    if not channels:
        console.print(Panel(
            "No Food Rescue channels available for this location.",
            title="[bold yellow]No Channels[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED
        ))
    else:
        print_success(f"Found {len(channels)} channel(s)")
        console.print()
        
        table = Table(box=box.SIMPLE_HEAD, header_style="bold yellow", border_style="dim")
        table.add_column("Channel Name", style="cyan", width=40)
        table.add_column("MQTT User", style="green")
        table.add_column("MQTT Password", style="white")
        
        for ch in channels:
            masked_pwd = ch['mqtt_password'][:4] + "•" * 8
            table.add_row(ch['channel_name'], ch['mqtt_username'], masked_pwd)
        
        console.print(Panel(table, title="[bold green]Live Food Rescue Channels[/bold green]", border_style="green", box=box.ROUNDED))
        console.print()
        print_success("Ready")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
