from paper_trading import (
    create_paper_portfolio,
    paper_buy,
    paper_sell,
    get_portfolio_summary,
)


def test_portfolio_summary_for_new_portfolio():
    portfolio = create_paper_portfolio()
    summary = get_portfolio_summary(portfolio)

    assert summary["cash"] == 10000.0
    assert summary["position_count"] == 0
    assert summary["tickers"] == []
    assert summary["trade_count"] == 0


def test_portfolio_summary_after_buy():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)

    summary = get_portfolio_summary(portfolio)

    assert summary["cash"] == 9500.0
    assert summary["position_count"] == 1
    assert summary["tickers"] == ["AAPL"]
    assert summary["trade_count"] == 1


def test_portfolio_summary_after_buy_and_sell():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)
    paper_sell(portfolio, "AAPL", 110, 2)

    summary = get_portfolio_summary(portfolio)

    assert summary["cash"] == 9720.0
    assert summary["position_count"] == 1
    assert summary["tickers"] == ["AAPL"]
    assert summary["trade_count"] == 2


def test_portfolio_summary_after_full_exit():
    portfolio = create_paper_portfolio()
    paper_buy(portfolio, "AAPL", 100, 5)
    paper_sell(portfolio, "AAPL", 110, 5)

    summary = get_portfolio_summary(portfolio)

    assert summary["cash"] == 10050.0
    assert summary["position_count"] == 0
    assert summary["tickers"] == []
    assert summary["trade_count"] == 2
    