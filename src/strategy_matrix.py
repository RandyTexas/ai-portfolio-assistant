STRATEGY_MATRIX = {
    "scalp_fast": {
        "take_profit_pct": 0.02,
        "stop_loss_pct": 0.01,
        "trailing_stop_pct": 0.01,
        "max_position_size_pct": 0.04,
        "description": "Fast trades with tight exits and smaller size.",
    },
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
    "swing_hold": {
        "take_profit_pct": 0.12,
        "stop_loss_pct": 0.05,
        "trailing_stop_pct": 0.04,
        "max_position_size_pct": 0.08,
        "description": "Longer swing holds with wider targets and moderate size.",
    },
}


def get_matrix_profile(name):
    return STRATEGY_MATRIX.get(name.strip().lower())


def list_matrix_profiles():
    return sorted(STRATEGY_MATRIX.keys())