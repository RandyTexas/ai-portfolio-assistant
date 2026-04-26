from paper_trading import (
    create_paper_portfolio,
    paper_buy,
    paper_sell,
    get_trade_history,
)


def test_trade_history_starts_empty():
    portfolio = create_paper_portfolio()
    history = get_trade_history(portfolio)

    assert history == []


def test_trade_history_after_buy():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    history = get_trade_history(portfolio)

    assert len(history) == 1
    assert history[0]["action"] == "BUY"
    assert history[0]["ticker"] == "AAPL"
    assert history[0]["price"] == 100.0
    assert history[0]["shares"] == 5
    assert history[0]["total"] == 500.0


def test_trade_history_after_buy_and_sell():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)
    paper_sell(portfolio, "AAPL", 110, 2)

    history = get_trade_history(portfolio)

    assert len(history) == 2

    assert history[0]["action"] == "BUY"
    assert history[0]["ticker"] == "AAPL"
    assert history[0]["total"] == 500.0

    assert history[1]["action"] == "SELL"
    assert history[1]["ticker"] == "AAPL"
    assert history[1]["total"] == 220.0


def test_trade_history_keeps_order():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)
    paper_buy(portfolio, "MSFT", 200, 2)
    paper_sell(portfolio, "AAPL", 110, 1)

    history = get_trade_history(portfolio)

    assert len(history) == 3
    assert history[0]["ticker"] == "AAPL"
    assert history[1]["ticker"] == "MSFT"
    assert history[2]["ticker"] == "AAPL"
    assert history[2]["action"] == "SELL"