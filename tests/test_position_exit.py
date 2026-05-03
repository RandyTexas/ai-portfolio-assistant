from paper_trading import create_paper_portfolio, paper_buy
from position_exit import evaluate_position_exit


def test_position_exit_rejects_missing_position():
    portfolio = create_paper_portfolio()

    result = evaluate_position_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=108,
        highest_price=110,
        take_profit_pct=0.08,
    )

    assert result["exit"] is False
    assert result["reason"] == "No open position found for AAPL."
    assert result["ticker"] == "AAPL"


def test_position_exit_triggers_take_profit():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = evaluate_position_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=108,
        highest_price=110,
        take_profit_pct=0.08,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "take_profit"
    assert result["ticker"] == "AAPL"
    assert result["shares"] == 5
    assert result["entry_price"] == 100.0


def test_position_exit_triggers_stop_loss():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = evaluate_position_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=95,
        highest_price=102,
        stop_loss_pct=0.05,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "stop_loss"
    assert result["reason"] == "Stop loss triggered."


def test_position_exit_triggers_trailing_stop():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = evaluate_position_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=105.6,
        highest_price=110,
        trailing_stop_pct=0.04,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "trailing_stop"
    assert result["reason"] == "Trailing stop triggered."


def test_position_exit_no_trigger():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    result = evaluate_position_exit(
        portfolio=portfolio,
        ticker="AAPL",
        current_price=103,
        highest_price=104,
        take_profit_pct=0.08,
        stop_loss_pct=0.05,
        trailing_stop_pct=0.04,
    )

    assert result["exit"] is False
    assert result["exit_type"] is None
    assert result["reason"] == "No exit rule triggered."