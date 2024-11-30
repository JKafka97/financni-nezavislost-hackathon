# Import libraries
import pandas as pd
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app"))
)
from calculation import calculate_fi_number, calculate_fi_metrics


################################################################################################
def test_calculate_fi_number_default_rate():
    assert calculate_fi_number(50000) == 15000000


def test_calculate_fi_number_custom_rate():
    assert calculate_fi_number(50000, safe_withdrawal_rate=5) == 12000000


def test_calculate_fi_number_zero_expenses():
    assert calculate_fi_number(0) == 0


def test_calculate_fi_number_large_expenses():
    assert calculate_fi_number(1000000) == 300000000


def test_calculate_fi_number_negative_expenses():
    # Handling negative expenses should return a negative FI number
    assert calculate_fi_number(-50000) == -15000000


################################################################################################


################################################################################################
def test_calculate_fi_metrics_standard_case():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=50000,
        current_savings=600000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics["initial_fi_target"] == 15000000
    assert metrics["years_to_fi"] is None
    assert isinstance(metrics["fire_data"], pd.DataFrame)
    assert metrics["monthly_savings_rate"] > 0


def test_calculate_fi_metrics_high_investment_return():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=50000,
        current_savings=600000,
        investment_return=20,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics["years_to_fi"] < 20


def test_calculate_fi_metrics_zero_expenses():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=0,
        current_savings=600000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics["years_to_fi"] == 0


def test_calculate_fi_metrics_high_expenses():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=100000,
        current_savings=600000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics["years_to_fi"] is None


################################################################################################
