STRATEGY_MATRIX = {
    "quick_trade": {
        "take_profit_pct": 0.03,
        "stop_loss_pct": 0.02,
        "trailing_stop_pct": 0.02,
        "max_position_size_pct": 0.05,
        "description": "Small fast moves with tighter exits.",
    },
    "short_hold": {
        "take_profit_pct": 0.08,
        "stop_loss_pct": 0.04,
        "trailing_stop_pct": 0.03,
        "max_position_size_pct": 0.10,
        "description": "Short-term holds with more room to move.",
    },
}


def get_matrix_profile(name):
    return STRATEGY_MATRIX.get(name.strip().lower())


def list_matrix_profiles():
    return sorted(STRATEGY_MATRIX.keys())