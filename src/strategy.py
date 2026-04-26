STRATEGY_PROFILES = {
    "balanced": {
        "take_profit_pct": 0.08,
        "trailing_stop_pct": 0.04,
        "stop_loss_pct": 0.05,
        "average_down_pct": 0.03,
        "max_average_downs": 1,
        "max_position_size_pct": 0.10,
    },
    "aggressive": {
        "take_profit_pct": 0.15,
        "trailing_stop_pct": 0.06,
        "stop_loss_pct": 0.08,
        "average_down_pct": 0.05,
        "max_average_downs": 2,
        "max_position_size_pct": 0.15,
    },
}


def get_strategy_profile(name):
    return STRATEGY_PROFILES.get(name.lower())