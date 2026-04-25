from watchlist import has_ticker, get_stock_by_ticker, get_categories


def test_has_ticker_finds_existing_stock():
    assert has_ticker("AAPL") is True


def test_has_ticker_returns_false_for_missing_stock():
    assert has_ticker("NVDA") is False


def test_get_stock_by_ticker_returns_stock_item():
    stock = get_stock_by_ticker("KO")
    assert stock == {"ticker": "KO", "category": "dividend"}


def test_get_stock_by_ticker_returns_none_for_missing_stock():
    assert get_stock_by_ticker("NVDA") is None


def test_get_categories_returns_expected_categories():
    categories = get_categories()
    assert "growth" in categories
    assert "dividend" in categories
    assert "reit" in categories
    assert "etf" in categories