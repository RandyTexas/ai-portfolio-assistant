from copy import deepcopy

import watchlist
from config.settings import DEFAULT_WATCHLIST
from research.stock_research import build_basic_stock_report


def reset_watchlist_file():
    watchlist.save_watchlist(deepcopy(DEFAULT_WATCHLIST))


def test_build_basic_stock_report_for_watchlist_match():
    reset_watchlist_file()
    report = build_basic_stock_report("AAPL")

    assert report["ticker"] == "AAPL"
    assert report["status"] == "watchlist match found"
    assert report["in_watchlist"] is True
    assert report["category_guess"] == "growth"
    assert "currently saved in the watchlist" in report["summary"]


def test_build_basic_stock_report_for_missing_ticker():
    reset_watchlist_file()
    report = build_basic_stock_report("NVDA")

    assert report["ticker"] == "NVDA"
    assert report["status"] == "research scaffold only"
    assert report["in_watchlist"] is False
    assert report["category_guess"] is None
    assert "No saved watchlist entry" in report["summary"]