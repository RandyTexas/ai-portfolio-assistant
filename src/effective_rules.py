from strategy import get_strategy_profile
from strategy_matrix import get_matrix_profile
from strategy_overrides import get_ticker_override


def build_effective_rules(risk_profile_name, trade_style_name=None, ticker=None):
    risk_profile = get_strategy_profile(risk_profile_name)

    if risk_profile is None:
        return None

    merged_rules = dict(risk_profile)

    if trade_style_name:
        trade_style = get_matrix_profile(trade_style_name)
        if trade_style is None:
            return None
        merged_rules.update(trade_style)

    if ticker:
        ticker_override = get_ticker_override(ticker)
        if ticker_override:
            merged_rules.update(ticker_override)

    return merged_rules