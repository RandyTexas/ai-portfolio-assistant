import json

import watchlist


def test_has_ticker_finds_existing_stock():
    assert watchlist.has_ticker("AAPL") is True


def test_has_ticker_returns_false_for_missing_stock():
    assert watchlist.has_ticker("NVDA") is False


def test_get_stock_by_ticker_returns_stock_item():
    stock = watchlist.get_stock_by_ticker("KO")
    assert stock == {"ticker": "KO", "category": "dividend"}


def test_get_stock_by_ticker_returns_none_for_missing_stock():
    assert watchlist.get_stock_by_ticker("NVDA") is None


def test_get_categories_returns_expected_categories():
    categories = watchlist.get_categories()
    assert "growth" in categories
    assert "dividend" in categories
    assert "reit" in categories
    assert "etf" in categories


def test_add_stock_adds_new_stock(tmp_path, monkeypatch):
    test_file = tmp_path / "watchlist.json"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(watchlist, "WATCHLIST_FILE", test_file)
    monkeypatch.setattr(watchlist, "DATA_DIR", test_data_dir)

    watchlist.save_watchlist(
        [
            {"ticker": "AAPL", "category": "growth"},
            {"ticker": "KO", "category": "dividend"},
        ]
    )

    result = watchlist.add_stock("NVDA", "growth")
    loaded = watchlist.load_watchlist()

    assert result is True
    assert {"ticker": "NVDA", "category": "growth"} in loaded


def test_add_stock_blocks_duplicate(tmp_path, monkeypatch):
    test_file = tmp_path / "watchlist.json"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(watchlist, "WATCHLIST_FILE", test_file)
    monkeypatch.setattr(watchlist, "DATA_DIR", test_data_dir)

    watchlist.save_watchlist(
        [
            {"ticker": "AAPL", "category": "growth"},
            {"ticker": "KO", "category": "dividend"},
        ]
    )

    result = watchlist.add_stock("AAPL", "growth")
    loaded = watchlist.load_watchlist()

    assert result is False
    assert len([item for item in loaded if item["ticker"] == "AAPL"]) == 1


def test_remove_stock_removes_existing_stock(tmp_path, monkeypatch):
    test_file = tmp_path / "watchlist.json"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(watchlist, "WATCHLIST_FILE", test_file)
    monkeypatch.setattr(watchlist, "DATA_DIR", test_data_dir)

    watchlist.save_watchlist(
        [
            {"ticker": "AAPL", "category": "growth"},
            {"ticker": "KO", "category": "dividend"},
        ]
    )

    result = watchlist.remove_stock("KO")
    loaded = watchlist.load_watchlist()

    assert result is True
    assert {"ticker": "KO", "category": "dividend"} not in loaded


def test_remove_stock_returns_false_for_missing_stock(tmp_path, monkeypatch):
    test_file = tmp_path / "watchlist.json"
    test_data_dir = tmp_path / "data"

    monkeypatch.setattr(watchlist, "WATCHLIST_FILE", test_file)
    monkeypatch.setattr(watchlist, "DATA_DIR", test_data_dir)

    watchlist.save_watchlist(
        [
            {"ticker": "AAPL", "category": "growth"},
            {"ticker": "KO", "category": "dividend"},
        ]
    )

    result = watchlist.remove_stock("NVDA")
    loaded = watchlist.load_watchlist()

    assert result is False
    assert {"ticker": "AAPL", "category": "growth"} in loaded
    assert {"ticker": "KO", "category": "dividend"} in loaded