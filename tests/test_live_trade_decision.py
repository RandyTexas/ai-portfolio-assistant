from live_trade_decision import evaluate_live_trade_with_effective_rules


def test_live_trade_decision_returns_error_when_no_bar(monkeypatch):
    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return None

    monkeypatch.setattr(
        "live_trade_decision.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    result = evaluate_live_trade_with_effective_rules(
        ticker="AAPL",
        risk_profile_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        trade_style_name="quick_trade",
        feed="iex",
    )

    assert result["approved"] is False
    assert result["reason"] == "No live market data returned for ticker."
    assert result["latest_bar"] is None


def test_live_trade_decision_uses_live_close_as_entry_price(monkeypatch):
    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return {
            "symbol": "AAPL",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 103.0,
            "volume": 1000,
        }

    monkeypatch.setattr(
        "live_trade_decision.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    result = evaluate_live_trade_with_effective_rules(
        ticker="AAPL",
        risk_profile_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        trade_style_name="quick_trade",
        feed="iex",
    )

    assert result["approved"] is True
    assert result["entry_price_used"] == 103.0
    assert result["latest_bar"]["close"] == 103.0
    assert result["max_position_size"] == 500.0


def test_live_trade_decision_rejects_oversized_trade(monkeypatch):
    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return {
            "symbol": "AAPL",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 103.0,
            "volume": 1000,
        }

    monkeypatch.setattr(
        "live_trade_decision.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    result = evaluate_live_trade_with_effective_rules(
        ticker="AAPL",
        risk_profile_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=600,
        trade_style_name="quick_trade",
        feed="iex",
    )

    assert result["approved"] is False
    assert result["reason"] == "Position size is too large for the merged effective rules."
    assert result["entry_price_used"] == 103.0


def test_live_trade_decision_uses_ticker_override(monkeypatch):
    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return {
            "symbol": "NVDA",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.0,
            "volume": 1000,
        }

    monkeypatch.setattr(
        "live_trade_decision.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    result = evaluate_live_trade_with_effective_rules(
        ticker="NVDA",
        risk_profile_name="balanced",
        portfolio_cash=10000,
        position_size_dollars=500,
        trade_style_name=None,
        feed="iex",
    )

    assert result["approved"] is True
    assert result["entry_price_used"] == 100.0
    assert result["stop_loss_price"] == 97.0
    assert result["take_profit_price"] == 110.0