import market_data


def test_get_latest_stock_bar_returns_formatted_bar(monkeypatch):
    def fake_fetch_json(url):
        return {
            "bar": {
                "t": "2026-05-04T19:59:00Z",
                "o": 100.0,
                "h": 101.5,
                "l": 99.5,
                "c": 101.0,
                "v": 123456,
            }
        }

    monkeypatch.setattr(market_data, "_fetch_json", fake_fetch_json)

    result = market_data.get_latest_stock_bar("aapl", feed="iex")

    assert result["symbol"] == "AAPL"
    assert result["timestamp"] == "2026-05-04T19:59:00Z"
    assert result["open"] == 100.0
    assert result["high"] == 101.5
    assert result["low"] == 99.5
    assert result["close"] == 101.0
    assert result["volume"] == 123456


def test_get_latest_stock_bar_returns_none_when_missing_bar(monkeypatch):
    def fake_fetch_json(url):
        return {}

    monkeypatch.setattr(market_data, "_fetch_json", fake_fetch_json)

    result = market_data.get_latest_stock_bar("AAPL")

    assert result is None


def test_get_latest_crypto_bar_returns_formatted_bar(monkeypatch):
    def fake_fetch_json(url):
        return {
            "bars": {
                "BTC/USD": {
                    "t": "2026-05-04T19:59:00Z",
                    "o": 60000.0,
                    "h": 60500.0,
                    "l": 59800.0,
                    "c": 60300.0,
                    "v": 42.5,
                }
            }
        }

    monkeypatch.setattr(market_data, "_fetch_json", fake_fetch_json)

    result = market_data.get_latest_crypto_bar("btc/usd")

    assert result["symbol"] == "BTC/USD"
    assert result["timestamp"] == "2026-05-04T19:59:00Z"
    assert result["open"] == 60000.0
    assert result["high"] == 60500.0
    assert result["low"] == 59800.0
    assert result["close"] == 60300.0
    assert result["volume"] == 42.5


def test_get_latest_crypto_bar_returns_none_when_missing_bar(monkeypatch):
    def fake_fetch_json(url):
        return {"bars": {}}

    monkeypatch.setattr(market_data, "_fetch_json", fake_fetch_json)

    result = market_data.get_latest_crypto_bar("BTC/USD")

    assert result is None


def test_refresh_watchlist_market_data_returns_results(monkeypatch):
    def fake_load_watchlist():
        return [
            {"ticker": "AAPL", "category": "growth"},
            {"ticker": "MSFT", "category": "growth"},
        ]

    def fake_get_latest_stock_bar(symbol, feed="iex"):
        return {
            "symbol": symbol,
            "timestamp": "2026-05-04T19:59:00Z",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "volume": 1000,
        }

    monkeypatch.setattr(market_data, "load_watchlist", fake_load_watchlist)
    monkeypatch.setattr(market_data, "get_latest_stock_bar", fake_get_latest_stock_bar)

    results = market_data.refresh_watchlist_market_data(feed="iex")

    assert len(results) == 2
    assert results[0]["ticker"] == "AAPL"
    assert results[0]["status"] == "ok"
    assert results[0]["bar"]["close"] == 100.5
    assert results[1]["ticker"] == "MSFT"
    assert results[1]["status"] == "ok"


def test_refresh_watchlist_market_data_handles_errors(monkeypatch):
    def fake_load_watchlist():
        return [{"ticker": "AAPL", "category": "growth"}]

    def fake_get_latest_stock_bar(symbol, feed="iex"):
        raise RuntimeError("API failure")

    monkeypatch.setattr(market_data, "load_watchlist", fake_load_watchlist)
    monkeypatch.setattr(market_data, "get_latest_stock_bar", fake_get_latest_stock_bar)

    results = market_data.refresh_watchlist_market_data(feed="iex")

    assert len(results) == 1
    assert results[0]["ticker"] == "AAPL"
    assert results[0]["status"] == "error"
    assert "API failure" in results[0]["error"]
    assert results[0]["bar"] is None