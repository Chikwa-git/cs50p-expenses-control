from project import get_date, get_expense, get_value


def test_get_date(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "2025-12-02")
    result = get_date()
    assert result.year == 2025
    assert result.month == 12
    assert result.day == 2


def test_get_date_invalid_then_valid(monkeypatch):
    inputs = iter(["02-01-2026", "2025-12-02"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_date()
    assert result.year == 2025


def test_get_expense_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: " arroz ")
    result = get_expense()
    assert result == "ARROZ"


def test_get_expense_empty_then_valid(monkeypatch):
    inputs = iter(["   ", "feijao"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_expense()
    assert result == "FEIJAO"


def test_get_value_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "12.5")
    result = get_value()
    assert result == 12.5


def test_get_value_invalid_then_valid(monkeypatch):
    inputs = iter(["abc", "15"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_value()
    assert result == 15.0


def test_get_value_zero_negative_then_valid(monkeypatch):
    inputs = iter(["0", "-3", "8"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = get_value()
    assert result == 8.0