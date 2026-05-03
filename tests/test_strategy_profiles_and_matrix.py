from strategy import get_strategy_profile
from strategy_matrix import get_matrix_profile, list_matrix_profiles


def test_passive_risk_profile_exists():
    profile = get_strategy_profile("passive")

    assert profile is not None
    assert profile["take_profit_pct"] == 0.05
    assert profile["stop_loss_pct"] == 0.03
    assert profile["max_average_downs"] == 0
    assert profile["max_position_size_pct"] == 0.05


def test_balanced_risk_profile_exists():
    profile = get_strategy_profile("balanced")

    assert profile is not None
    assert profile["take_profit_pct"] == 0.08
    assert profile["stop_loss_pct"] == 0.05
    assert profile["max_average_downs"] == 1
    assert profile["max_position_size_pct"] == 0.10


def test_aggressive_risk_profile_exists():
    profile = get_strategy_profile("aggressive")

    assert profile is not None
    assert profile["take_profit_pct"] == 0.15
    assert profile["stop_loss_pct"] == 0.08
    assert profile["max_average_downs"] == 2
    assert profile["max_position_size_pct"] == 0.15


def test_unknown_risk_profile_returns_none():
    profile = get_strategy_profile("unknown")

    assert profile is None


def test_quick_trade_matrix_profile_exists():
    profile = get_matrix_profile("quick_trade")

    assert profile is not None
    assert profile["take_profit_pct"] == 0.03
    assert profile["stop_loss_pct"] == 0.02
    assert profile["trailing_stop_pct"] == 0.02
    assert profile["max_position_size_pct"] == 0.05


def test_short_hold_matrix_profile_exists():
    profile = get_matrix_profile("short_hold")

    assert profile is not None
    assert profile["take_profit_pct"] == 0.08
    assert profile["stop_loss_pct"] == 0.04
    assert profile["trailing_stop_pct"] == 0.03
    assert profile["max_position_size_pct"] == 0.10


def test_unknown_matrix_profile_returns_none():
    profile = get_matrix_profile("unknown")

    assert profile is None


def test_list_matrix_profiles_returns_expected_names():
    profiles = list_matrix_profiles()

    assert "quick_trade" in profiles
    assert "short_hold" in profiles