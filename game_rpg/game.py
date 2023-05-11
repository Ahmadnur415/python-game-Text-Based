from rich.console import Console

__all__ = "__version__", "console"

__version__ = "1.0.0"

console = Console(color_system="truecolor", force_terminal=True, tab_size=4)
