def evaluate_exit_rules(
    entry_price,
    current_price,
    highest_price,
    take_profit_pct=None,
    take_profit_price=None,
    stop_loss_pct=None,
    stop_loss_price=None,
    trailing_stop_pct=None,
    trailing_stop_amount=None,
):
    if entry_price <= 0 or current_price <= 0 or highest_price <= 0:
        return {
            "exit": False,
            "reason": "Prices must be greater than 0.",
        }

    def pct_take_profit_price():
        if take_profit_pct is None:
            return None
        return entry_price * (1 + take_profit_pct)

    def pct_stop_loss_price():
        if stop_loss_pct is None:
            return None
        return entry_price * (1 - stop_loss_pct)

    def pct_trailing_stop_price():
        if trailing_stop_pct is None:
            return None
        return highest_price * (1 - trailing_stop_pct)

    def amt_trailing_stop_price():
        if trailing_stop_amount is None:
            return None
        return highest_price - trailing_stop_amount

    take_profit_candidates = []
    if pct_take_profit_price() is not None:
        take_profit_candidates.append(pct_take_profit_price())
    if take_profit_price is not None:
        take_profit_candidates.append(float(take_profit_price))

    stop_loss_candidates = []
    if pct_stop_loss_price() is not None:
        stop_loss_candidates.append(pct_stop_loss_price())
    if stop_loss_price is not None:
        stop_loss_candidates.append(float(stop_loss_price))

    trailing_stop_candidates = []
    if pct_trailing_stop_price() is not None:
        trailing_stop_candidates.append(pct_trailing_stop_price())
    if amt_trailing_stop_price() is not None:
        trailing_stop_candidates.append(amt_trailing_stop_price())

    active_take_profit_price = min(take_profit_candidates) if take_profit_candidates else None
    active_stop_loss_price = max(stop_loss_candidates) if stop_loss_candidates else None
    active_trailing_stop_price = max(trailing_stop_candidates) if trailing_stop_candidates else None

    if active_take_profit_price is not None and current_price >= active_take_profit_price:
        return {
            "exit": True,
            "reason": "Take profit target reached.",
            "exit_type": "take_profit",
            "active_take_profit_price": round(active_take_profit_price, 2),
            "active_stop_loss_price": round(active_stop_loss_price, 2) if active_stop_loss_price is not None else None,
            "active_trailing_stop_price": round(active_trailing_stop_price, 2) if active_trailing_stop_price is not None else None,
        }

    if active_stop_loss_price is not None and current_price <= active_stop_loss_price:
        return {
            "exit": True,
            "reason": "Stop loss triggered.",
            "exit_type": "stop_loss",
            "active_take_profit_price": round(active_take_profit_price, 2) if active_take_profit_price is not None else None,
            "active_stop_loss_price": round(active_stop_loss_price, 2),
            "active_trailing_stop_price": round(active_trailing_stop_price, 2) if active_trailing_stop_price is not None else None,
        }

    if active_trailing_stop_price is not None and current_price <= active_trailing_stop_price:
        return {
            "exit": True,
            "reason": "Trailing stop triggered.",
            "exit_type": "trailing_stop",
            "active_take_profit_price": round(active_take_profit_price, 2) if active_take_profit_price is not None else None,
            "active_stop_loss_price": round(active_stop_loss_price, 2) if active_stop_loss_price is not None else None,
            "active_trailing_stop_price": round(active_trailing_stop_price, 2),
        }

    return {
        "exit": False,
        "reason": "No exit rule triggered.",
        "exit_type": None,
        "active_take_profit_price": round(active_take_profit_price, 2) if active_take_profit_price is not None else None,
        "active_stop_loss_price": round(active_stop_loss_price, 2) if active_stop_loss_price is not None else None,
        "active_trailing_stop_price": round(active_trailing_stop_price, 2) if active_trailing_stop_price is not None else None,
    }