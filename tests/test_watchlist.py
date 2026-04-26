import json
from copy import deepcopy

import watchlist
from config.settings import DEFAULT_WATCHLIST


def reset_watchlist_file():
    watchlist.save_watchlist(deepcopy(DEFAULT_WATCHLIST))


def test_get_ticker_symbols():
    reset_watchlist_file()
    symbols = watchlist.get_ticker_symbols()
    assert symbols == ["AAPL", "MSFT", "KO", "O", "SPY"]


def test_has_ticker():
    reset_watchlist_file()
    assert watchlist.has_ticker("AAPL") is True
    assert watchlist.has_ticker("NVDA") is False


def test_get_stock_by_ticker():
    reset_watchlist_file()
    stock = watchlist.get_stock_by_ticker("KO")
    assert stock == {"ticker": "KO", "category": "dividend"}
    assert watchlist.get_stock_by_ticker("NVDA") is None


def test_get_stocks_by_category():
    reset_watchlist_file()
    growth_stocks = watchlist.get_stocks_by_category("growth")
    assert growth_stocks == [
        {"ticker": "AAPL", "category": "growth"},
        {"ticker": "MSFT", "category": "growth"},
    ]


def test_add_stock():
    reset_watchlist_file()
    added = watchlist.add_stock("NVDA", "growth")
    assert added is True
    assert watchlist.has_ticker("NVDA") is True


def test_add_stock_blocks_duplicates():
    reset_watchlist_file()
    first_add = watchlist.add_stock("NVDA", "growth")
    second_add = watchlist.add_stock("NVDA", "growth")
    assert first_add is True
    assert second_add is False


def test_remove_stock():
    reset_watchlist_file()
    removed = watchlist.remove_stock("KO")
    assert removed is True
    assert watchlist.has_ticker("KO") is False


def test_remove_stock_returns_false_for_missing_ticker():
    reset_watchlist_file()
    removed = watchlist.remove_stock("NVDA")
    assert removed is False


def test_get_categories():
    reset_watchlist_file()
    categories = watchlist.get_categories()
    assert categories == ["dividend", "etf", "growth", "reit"]