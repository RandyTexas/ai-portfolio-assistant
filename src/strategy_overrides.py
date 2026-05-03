from strategy import get_strategy_profile


TICKER_OVERRIDES = {
    "NVDA": {
        "take_profit_pct": 0.10,
        "stop_loss_pct": 0.03,
        "trailing_stop_pct": 0.03,
    },
    "BTC": {
        "take_profit_pct": 0.12,
        "stop_loss_pct": 0.05,
        "trailing_stop_pct": 0.04,
        "max_position_size_pct": 0.08,
    },
}


def get_ticker_override(ticker):
    return TICKER_OVERRIDES.get(ticker.strip().upper())


def get_effective_strategy(strategy_name, ticker=None):
    base_profile = get_strategy_profile(strategy_name)

    if base_profile is None:
        return None

    merged_profile = dict(base_profile)

    if ticker:
        override = get_ticker_override(ticker)
        if override:
            merged_profile.update(override)

    return merged_profile