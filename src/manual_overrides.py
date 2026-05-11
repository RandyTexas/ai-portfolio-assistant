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


def list_manual_ticker_overrides():
    store = load_ticker_override_store()
    results = []

    for ticker, data in store.items():
        results.append(
            {
                "ticker": ticker,
                "name": data.get("name", f"{ticker} manual override"),
                "enabled": data.get("enabled", True),
                "rules": data.get("rules", {}),
            }
        )

    return results


def update_manual_ticker_override(ticker, updated_fields):
    ticker = ticker.strip().upper()
    store = load_ticker_override_store()

    if ticker not in store:
        return None

    current = store[ticker]
    current_rules = current.get("rules", {})

    if "name" in updated_fields and updated_fields["name"] is not None:
        current["name"] = updated_fields["name"].strip()

    for rule_key in (
        "take_profit_pct",
        "stop_loss_pct",
        "trailing_stop_pct",
        "max_position_size_pct",
    ):
        if rule_key in updated_fields and updated_fields[rule_key] is not None:
            current_rules[rule_key] = updated_fields[rule_key]

    current["rules"] = current_rules
    store[ticker] = current
    save_ticker_override_store(store)

    return {
        "ticker": ticker,
        "updated_override": store[ticker],
    }