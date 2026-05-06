import market_data
from live_trade_decision import evaluate_live_trade_with_effective_rules
from live_trade_execution import execute_live_trade_with_effective_rules
from paper_trading import create_paper_portfolio


def test_get_latest_market_bar_routes_to_crypto(monkeypatch):
    def fake_get_latest_crypto_bar(symbol, loc=None):
        return {
            "symbol": "BTC/USD",
            "asset_type": "crypto",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 60000.0,
            "high": 60500.0,
            "low": 59800.0,
            "close": 60300.0,
            "volume": 42.5,
        }

    monkeypatch.setattr(
        market_data,
        "get_latest_crypto_bar",
        fake_get_latest_crypto_bar,
    )

    result = market_data.get_latest_market_bar("BTC/USD")

    assert result["symbol"] == "BTC/USD"
    assert result["asset_type"] == "crypto"
    assert result["close"] == 60300.0


def test_get_latest_market_bar_routes_to_stock(monkeypatch):
    def fake_get_latest_stock_bar(symbol, feed="iex"):
        return {
            "symbol": "AAPL",
            "asset_type": "stock",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "volume": 1000,
        }

    monkeypatch.setattr(
        market_data,
        "get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    result = market_data.get_latest_market_bar("AAPL", feed="iex")

    assert result["symbol"] == "AAPL"
    assert result["asset_type"] == "stock"
    assert result["close"] == 100.5


def test_live_trade_decision_works_for_crypto(monkeypatch):
    def fake_get_latest_market_bar(ticker, feed="iex"):
        return {
            "symbol": "BTC/USD",
            "asset_type": "crypto",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 60000.0,
            "high": 60500.0,
            "low": 59800.0,
            "close": 60300.0,
            "volume": 42.5,
        }

    monkeypatch.setattr(
        "live_trade_decision.get_latest_market_bar",
        fake_get_latest_market_bar,
    )

    result = evaluate_live_trade_with_effective_rules(
        ticker="BTC/USD",
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=100000,
        position_size_dollars=500,
        feed="iex",
    )

    assert result["approved"] is True
    assert result["latest_bar"]["asset_type"] == "crypto"
    assert result["entry_price_used"] == 60300.0


def test_live_trade_execution_works_for_crypto(monkeypatch):
    def fake_get_latest_market_bar(ticker, feed="iex"):
        return {
            "symbol": "BTC/USD",
            "asset_type": "crypto",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 60000.0,
            "high": 60500.0,
            "low": 59800.0,
            "close": 100.0,
            "volume": 42.5,
        }

    monkeypatch.setattr(
        "live_trade_execution.get_latest_market_bar",
        fake_get_latest_market_bar,
    )

    portfolio = create_paper_portfolio()

    result = execute_live_trade_with_effective_rules(
        portfolio=portfolio,
        ticker="BTC/USD",
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=10000,
        position_size_dollars=500,
        feed="iex",
    )

    assert result["executed"] is True
    assert result["entry_price_used"] == 100.0
    assert result["shares_bought"] == 5
    assert "BTC/USD" in portfolio["positions"]


def test_live_trade_execution_returns_error_when_no_market_data(monkeypatch):
    def fake_get_latest_market_bar(ticker, feed="iex"):
        return None

    monkeypatch.setattr(
        "live_trade_execution.get_latest_market_bar",
        fake_get_latest_market_bar,
    )

    portfolio = create_paper_portfolio()

    result = execute_live_trade_with_effective_rules(
        portfolio=portfolio,
        ticker="BTC/USD",
        risk_profile_name="balanced",
        trade_style_name="quick_trade",
        portfolio_cash=10000,
        position_size_dollars=500,
        feed="iex",
    )

    assert result["executed"] is False
    assert result["reason"] == "No live market data returned for ticker."
    assert result["latest_bar"] is None