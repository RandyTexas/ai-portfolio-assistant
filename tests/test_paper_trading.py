from paper_trading import create_paper_portfolio, paper_buy, paper_sell


def test_create_paper_portfolio():
    portfolio = create_paper_portfolio()
    assert portfolio["cash"] == 10000.0
    assert portfolio["positions"] == {}
    assert portfolio["trade_history"] == []


def test_paper_buy_success():
    portfolio = create_paper_portfolio()
    success, message = paper_buy(portfolio, "AAPL", 100, 5)

    assert success is True
    assert portfolio["cash"] == 9500.0
    assert portfolio["positions"]["AAPL"]["shares"] == 5
    assert portfolio["positions"]["AAPL"]["average_price"] == 100.0
    assert portfolio["trade_history"][0]["action"] == "BUY"


def test_paper_buy_fails_with_not_enough_cash():
    portfolio = create_paper_portfolio()
    success, message = paper_buy(portfolio, "AAPL", 5000, 3)

    assert success is False
    assert message == "Not enough cash."
    assert portfolio["cash"] == 10000.0
    assert portfolio["positions"] == {}


def test_paper_sell_success():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    success, message = paper_sell(portfolio, "AAPL", 110, 2)

    assert success is True
    assert portfolio["cash"] == 9720.0
    assert portfolio["positions"]["AAPL"]["shares"] == 3
    assert portfolio["trade_history"][-1]["action"] == "SELL"


def test_paper_sell_fails_with_too_many_shares():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 2)

    success, message = paper_sell(portfolio, "AAPL", 110, 5)

    assert success is False
    assert message == "Not enough shares of AAPL to sell."


def test_paper_sell_fails_when_position_missing():
    portfolio = create_paper_portfolio()

    success, message = paper_sell(portfolio, "AAPL", 110, 1)

    assert success is False
    assert message == "No position found for AAPL."
    