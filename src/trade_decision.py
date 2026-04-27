from strategy_rules import evaluate_trade_setup


def evaluate_paper_trade_decision(
    strategy_name,
    portfolio_cash,
    position_size_dollars,
    entry_price,
    stop_loss_price,
    take_profit_price,
):
    evaluation = evaluate_trade_setup(
        strategy_name=strategy_name,
        portfolio_cash=portfolio_cash,
        position_size_dollars=position_size_dollars,
        entry_price=entry_price,
        stop_loss_price=stop_loss_price,
        take_profit_price=take_profit_price,
    )

    if evaluation["approved"] is False:
        return {
            "approved_for_paper_trade": False,
            "reason": evaluation["reason"],
            "evaluation": evaluation,
        }

    return {
        "approved_for_paper_trade": True,
        "reason": "Trade approved for paper trading.",
        "evaluation": evaluation,
    }