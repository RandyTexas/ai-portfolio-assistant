from strategy import get_strategy_profile


def evaluate_trade_setup(
    strategy_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    stop_loss_price,
    take_profit_price,
):
    profile = get_strategy_profile(strategy_name)

    if profile is None:
        return {
            "approved": False,
            "reason": "Strategy profile not found.",
        }

    if portfolio_cash <= 0:
        return {
            "approved": False,
            "reason": "Portfolio cash must be greater than 0.",
        }

    if entry_price <= 0 or stop_loss_price <= 0 or take_profit_price <= 0:
        return {
            "approved": False,
            "reason": "Prices must be greater than 0.",
        }

    max_position_size = portfolio_cash * profile["max_position_size_pct"]
    stop_loss_pct = (entry_price - stop_loss_price) / entry_price
    take_profit_pct = (take_profit_price - entry_price) / entry_price

    if position_size_dollars > max_position_size:
        return {
            "approved": False,
            "reason": "Position size is too large for this strategy.",
        }

    if stop_loss_pct > profile["stop_loss_pct"]:
        return {
            "approved": False,
            "reason": "Stop loss is wider than allowed for this strategy.",
        }

    if take_profit_pct < profile["take_profit_pct"]:
        return {
            "approved": False,
            "reason": "Take profit target is smaller than the strategy requires.",
        }

    return {
        "approved": True,
        "reason": "Trade setup passes the basic strategy checks.",
        "max_position_size": round(max_position_size, 2),
        "stop_loss_pct": round(stop_loss_pct, 4),
        "take_profit_pct": round(take_profit_pct, 4),
    }
