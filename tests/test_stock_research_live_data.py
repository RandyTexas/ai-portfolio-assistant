from research.stock_research import build_basic_stock_report


def test_build_basic_stock_report_for_watchlist_match(monkeypatch):
    def fake_get_stock_by_ticker(ticker):
        return {"ticker": "AAPL", "category": "growth"}

    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return {
            "symbol": "AAPL",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 100.0,
            "high": 101.0,
            "low": 99.5,
            "close": 100.5,
            "volume": 12345,
        }

    monkeypatch.setattr(
        "research.stock_research.get_stock_by_ticker",
        fake_get_stock_by_ticker,
    )
    monkeypatch.setattr(
        "research.stock_research.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    report = build_basic_stock_report("AAPL", feed="iex")

    assert report["ticker"] == "AAPL"
    assert report["in_watchlist"] is True
    assert report["category_guess"] == "growth"
    assert report["market_data_status"] == "ok"
    assert report["latest_bar"]["close"] == 100.5


def test_build_basic_stock_report_for_missing_watchlist_match(monkeypatch):
    def fake_get_stock_by_ticker(ticker):
        return None

    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return {
            "symbol": "XYZ",
            "timestamp": "2026-05-05T20:00:00Z",
            "open": 10.0,
            "high": 10.5,
            "low": 9.8,
            "close": 10.2,
            "volume": 5000,
        }

    monkeypatch.setattr(
        "research.stock_research.get_stock_by_ticker",
        fake_get_stock_by_ticker,
    )
    monkeypatch.setattr(
        "research.stock_research.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    report = build_basic_stock_report("XYZ", feed="iex")

    assert report["ticker"] == "XYZ"
    assert report["in_watchlist"] is False
    assert report["category_guess"] is None
    assert report["market_data_status"] == "ok"
    assert report["latest_bar"]["close"] == 10.2


def test_build_basic_stock_report_handles_no_market_data(monkeypatch):
    def fake_get_stock_by_ticker(ticker):
        return {"ticker": "AAPL", "category": "growth"}

    def fake_get_latest_stock_bar(ticker, feed="iex"):
        return None

    monkeypatch.setattr(
        "research.stock_research.get_stock_by_ticker",
        fake_get_stock_by_ticker,
    )
    monkeypatch.setattr(
        "research.stock_research.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    report = build_basic_stock_report("AAPL", feed="iex")

    assert report["market_data_status"] == "no_data"
    assert report["latest_bar"] is None


def test_build_basic_stock_report_handles_market_data_error(monkeypatch):
    def fake_get_stock_by_ticker(ticker):
        return {"ticker": "AAPL", "category": "growth"}

    def fake_get_latest_stock_bar(ticker, feed="iex"):
        raise RuntimeError("API failure")

    monkeypatch.setattr(
        "research.stock_research.get_stock_by_ticker",
        fake_get_stock_by_ticker,
    )
    monkeypatch.setattr(
        "research.stock_research.get_latest_stock_bar",
        fake_get_latest_stock_bar,
    )

    report = build_basic_stock_report("AAPL", feed="iex")

    assert report["market_data_status"].startswith("error:")
    assert "API failure" in report["market_data_status"]
    assert report["latest_bar"] is None