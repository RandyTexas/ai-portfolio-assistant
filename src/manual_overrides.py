import json

from config.settings import DATA_DIR, TICKER_OVERRIDE_STORE_FILE


def ensure_ticker_override_store():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not TICKER_OVERRIDE_STORE_FILE.exists():
        with TICKER_OVERRIDE_STORE_FILE.open("w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)


def load_ticker_override_store():
    ensure_ticker_override_store()

    with TICKER_OVERRIDE_STORE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_ticker_override_store(store):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with TICKER_OVERRIDE_STORE_FILE.open("w", encoding="utf-8") as file:
        json.dump(store, file, indent=4)


def save_manual_ticker_override(ticker, override_rules, name=None):
    ticker = ticker.strip().upper()
    store = load_ticker_override_store()

    existing = store.get(ticker, {})
    enabled = existing.get("enabled", True)
    override_name = name.strip() if name else f"{ticker} manual override"

    store[ticker] = {
        "name": override_name,
        "enabled": enabled,
        "rules": dict(override_rules),
    }

    save_ticker_override_store(store)

    return {
        "ticker": ticker,
        "saved_override": store[ticker],
    }


def get_manual_ticker_override(ticker):
    ticker = ticker.strip().upper()
    store = load_ticker_override_store()
    return store.get(ticker)


def has_manual_ticker_override(ticker):
    return get_manual_ticker_override(ticker) is not None


def delete_manual_ticker_override(ticker):
    ticker = ticker.strip().upper()
    store = load_ticker_override_store()

    if ticker not in store:
        return False

    del store[ticker]
    save_ticker_override_store(store)
    return True


def disable_manual_ticker_override(ticker):
    ticker = ticker.strip().upper()
    store = load_ticker_override_store()

    if ticker not in store:
        return False

    store[ticker]["enabled"] = False
    save_ticker_override_store(store)
    return True


def enable_manual_ticker_override(ticker):
    ticker = ticker.strip().upper()
    store = load_ticker_override_store()

    if ticker not in store:
        return False

    store[ticker]["enabled"] = True
    save_ticker_override_store(store)
    return True