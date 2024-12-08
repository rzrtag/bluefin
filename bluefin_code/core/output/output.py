"""Output formatting helpers."""

from colorama import Fore, Style
from typing import Dict, Any

def print_header(text: str):
    """Print a header with double lines."""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def print_section(text: str):
    """Print a section header with single line."""
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)

def print_subsection(text: str):
    """Print a subsection header."""
    print(f"\n{text}")
    print("-" * len(text))

def print_warning(text: str):
    """Print a warning message."""
    print(f"\033[93m⚠️  {text}\033[0m")

def print_success(text: str):
    """Print a success message."""
    print(f"\033[92m✓ {text}\033[0m")

def format_change(old: float, new: float, prec: int = 1) -> str:
    """Format value change with color."""
    diff = new - old
    if diff > 0:
        return f"{Fore.GREEN}+{diff:.{prec}f}{Style.RESET_ALL}"
    elif diff < 0:
        return f"{Fore.RED}{diff:.{prec}f}{Style.RESET_ALL}"
    return f"{diff:.{prec}f}"

def format_player_update(name: str, updates: Dict[str, tuple[float, float]]) -> str:
    """Format player update line."""
    parts = [f"{Fore.CYAN}{name}{Style.RESET_ALL}"]
    for stat, (old, new) in updates.items():
        change = format_change(old, new)
        parts.append(f"{stat}:{old:.1f}→{new:.1f}({change})")
    return " ".join(parts)  # All on one line
  