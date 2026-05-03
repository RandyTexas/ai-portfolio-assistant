from exit_rules import evaluate_exit_rules


def test_take_profit_by_percent_triggers():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=108,
        highest_price=110,
        take_profit_pct=0.08,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "take_profit"
    assert result["reason"] == "Take profit target reached."
    assert result["active_take_profit_price"] == 108.0


def test_take_profit_by_fixed_price_triggers():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=108,
        highest_price=110,
        take_profit_price=108,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "take_profit"
    assert result["active_take_profit_price"] == 108.0


def test_take_profit_uses_whichever_comes_first():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=108,
        highest_price=110,
        take_profit_pct=0.10,
        take_profit_price=108,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "take_profit"
    assert result["active_take_profit_price"] == 108.0


def test_stop_loss_by_percent_triggers():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=95,
        highest_price=102,
        stop_loss_pct=0.05,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "stop_loss"
    assert result["reason"] == "Stop loss triggered."
    assert result["active_stop_loss_price"] == 95.0


def test_stop_loss_by_fixed_price_triggers():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=96,
        highest_price=102,
        stop_loss_price=96,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "stop_loss"
    assert result["active_stop_loss_price"] == 96.0


def test_stop_loss_uses_whichever_comes_first():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=96,
        highest_price=102,
        stop_loss_pct=0.05,
        stop_loss_price=96,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "stop_loss"
    assert result["active_stop_loss_price"] == 96.0


def test_trailing_stop_by_percent_triggers():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=105.6,
        highest_price=110,
        trailing_stop_pct=0.04,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "trailing_stop"
    assert result["reason"] == "Trailing stop triggered."
    assert result["active_trailing_stop_price"] == 105.6


def test_trailing_stop_by_amount_triggers():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=105,
        highest_price=110,
        trailing_stop_amount=5,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "trailing_stop"
    assert result["active_trailing_stop_price"] == 105.0


def test_trailing_stop_uses_whichever_comes_first():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=106,
        highest_price=110,
        trailing_stop_pct=0.05,
        trailing_stop_amount=4,
    )

    assert result["exit"] is True
    assert result["exit_type"] == "trailing_stop"
    assert result["active_trailing_stop_price"] == 106.0


def test_no_exit_rule_triggered():
    result = evaluate_exit_rules(
        entry_price=100,
        current_price=103,
        highest_price=104,
        take_profit_pct=0.08,
        stop_loss_pct=0.05,
        trailing_stop_pct=0.04,
    )

    assert result["exit"] is False
    assert result["exit_type"] is None
    assert result["reason"] == "No exit rule triggered."