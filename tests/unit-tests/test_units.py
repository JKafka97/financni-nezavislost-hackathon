from app.utils import format_currency, format_time


# Test for format_currency function
def test_format_currency_integer():
    assert format_currency(1000) == "1 000 CZK"


def test_format_currency_float():
    assert format_currency(1234.56) == "1 235 CZK"


def test_format_currency_small_value():
    assert format_currency(999) == "999 CZK"


def test_format_currency_zero():
    assert format_currency(0) == "0 CZK"


def test_format_currency_large_value():
    assert format_currency(1000000) == "1 000 000 CZK"


# Test for format_time function
def test_format_time_none():
    assert format_time(None) == "Více než 50 let"


def test_format_time_integer_years():
    assert format_time(3) == "3r 0m"


def test_format_time_float_years_with_months():
    assert format_time(2.5) == "2r 6m"


def test_format_time_exactly_12_months():
    assert format_time(2.999) == "3r 0m"


def test_format_time_edge_case_50_years():
    assert format_time(50) == "50r 0m"
