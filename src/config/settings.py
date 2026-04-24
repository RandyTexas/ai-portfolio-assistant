from pathlib import Path

APP_NAME = "AI Portfolio Assistant"
VERSION = "0.2.0"
DEFAULT_MODE = "paper"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
WATCHLIST_FILE = DATA_DIR / "watchlist.json"

DEFAULT_WATCHLIST = [
    {"ticker": "AAPL", "category": "growth"},
    {"ticker": "MSFT", "category": "growth"},
    {"ticker": "KO", "category": "dividend"},
    {"ticker": "O", "category": "reit"},
    {"ticker": "SPY", "category": "etf"},
]