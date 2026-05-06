from pathlib import Path

APP_NAME = "AI Portfolio Assistant"
VERSION = "0.2.0"
DEFAULT_MODE = "paper"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

WATCHLIST_FILE = DATA_DIR / "watchlist.json"
CHANGE_REQUESTS_FILE = DATA_DIR / "change_requests.json"
IMPLEMENTATION_QUEUE_FILE = DATA_DIR / "implementation_queue.json"
TICKER_OVERRIDE_STORE_FILE = DATA_DIR / "ticker_overrides_store.json"

ALPACA_DATA_BASE_URL = "https://data.alpaca.markets"
ALPACA_CRYPTO_LOC = "us"

DEFAULT_WATCHLIST = [
    {"ticker": "AAPL", "category": "growth"},
    {"ticker": "MSFT", "category": "growth"},
    {"ticker": "KO", "category": "dividend"},
    {"ticker": "O", "category": "reit"},
    {"ticker": "SPY", "category": "etf"},
]