from market_data import get_latest_market_bar
from merged_trade_execution import execute_trade_with_effective_rules


def execute_live_trade_with_effective_rules(
    portfolio,
    ticker,
    risk_profile_name,
    portfolio_cash,
    position_size_dollars,
    trade_style_name=None,
    feed="iex",
):
    latest_bar = get_latest_market_bar(ticker, feed=feed)

    if latest_bar is None:
        return {
            "executed": False,
            "reason": "No live market data returned for ticker.",
            "latest_bar": None,
        }

    entry_price = latest_bar["close"]

    result = execute_trade_with_effective_rules(
        portfolio=portfolio,
        ticker=ticker,
        risk_profile_name=risk_profile_name,
        trade_style_name=trade_style_name,
        portfolio_cash=portfolio_cash,
        position_size_dollars=position_size_dollars,
        entry_price=entry_price,
    )

    return {
        **result,
        "latest_bar": latest_bar,
        "entry_price_used": entry_price,
    }