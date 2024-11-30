import pandas as pd
import pytest
from app.calculation import calculate_fi_number, calculate_fi_metrics


# Test cases for calculate_fi_number
@pytest.mark.parametrize(
    "monthly_expenses, safe_withdrawal_rate, expected",
    [
        (25000, 4, 7_500_000),  # Standard case
        (30000, 5, 7_200_000),  # Different withdrawal rate
        (0, 4, 0),  # Zero expenses
        (10000, 3, 4_000_000),  # High withdrawal rate
    ],
)
def test_calculate_fi_number(monthly_expenses, safe_withdrawal_rate, expected):
    assert calculate_fi_number(monthly_expenses, safe_withdrawal_rate) == expected


# Test cases for calculate_fi_metrics
def test_calculate_fi_metrics_nominal_values():
    result = calculate_fi_metrics(
        monthly_savings=15000,
        monthly_expenses=25000,
        current_savings=500_000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
        max_years=30,
    )

    assert result["initial_fi_target"] == pytest.approx(7_500_000)  # FI number
    assert result["monthly_savings_rate"] == pytest.approx(37.5)  # Savings rate
    assert isinstance(result["fire_data"], pd.DataFrame)  # Ensure output is a DataFrame


def test_calculate_fi_metrics_no_fi():
    result = calculate_fi_metrics(
        monthly_savings=1000,  # Low savings
        monthly_expenses=50000,  # High expenses
        current_savings=0,  # No initial savings
        investment_return=5,
        inflation_rate=3,
        safe_withdrawal_rate=4,
        max_years=30,
    )

    assert result["initial_fi_target"] == pytest.approx(15_000_000)  # FI target
    assert result["years_to_fi"] is None  # FI is not achievable
    assert result["monthly_savings_rate"] == pytest.approx(
        2.0, rel=2e-2
    )  # Allow 2% relative tolerance


def test_calculate_fi_metrics_high_return():
    result = calculate_fi_metrics(
        monthly_savings=20000,
        monthly_expenses=20000,
        current_savings=1_000_000,
        investment_return=10,  # High returns
        inflation_rate=2,  # Low inflation
        safe_withdrawal_rate=4,
        max_years=20,
    )

    assert result["initial_fi_target"] == pytest.approx(6_000_000)  # FI target
    assert result["years_to_fi"] is not None  # FI should be achievable
    assert result["years_to_fi"] < 20  # Should achieve FI sooner


def test_calculate_fi_metrics_output_structure():
    result = calculate_fi_metrics(
        monthly_savings=15000,
        monthly_expenses=25000,
        current_savings=500_000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
        max_years=30,
    )

    fire_data = result["fire_data"]

    # Check DataFrame structure
    assert "years" in fire_data.columns
    assert "portfolio_nominal" in fire_data.columns
    assert "portfolio_real" in fire_data.columns
    assert "expenses_annual" in fire_data.columns
    assert "fi_target" in fire_data.columns

    # Check values are non-negative
    assert (fire_data["portfolio_nominal"] >= 0).all()
    assert (fire_data["portfolio_real"] >= 0).all()
    assert (fire_data["expenses_annual"] >= 0).all()
    assert (fire_data["fi_target"] >= 0).all()


def test_calculate_fi_metrics_zero_savings():
    result = calculate_fi_metrics(
        monthly_savings=0,  # No savings
        monthly_expenses=20000,
        current_savings=500_000,
        investment_return=5,
        inflation_rate=3,
        safe_withdrawal_rate=4,
        max_years=30,
    )

    assert result["initial_fi_target"] == pytest.approx(6_000_000)  # FI target
    assert result["years_to_fi"] is None  # FI is not achievable with zero savings
    assert result["monthly_savings_rate"] == pytest.approx(0.0)  # Zero savings rate


def test_calculate_fi_metrics_inflation_exceeds_return():
    result = calculate_fi_metrics(
        monthly_savings=20000,
        monthly_expenses=20000,
        current_savings=1_000_000,
        investment_return=2,  # Low returns
        inflation_rate=3,  # High inflation
        safe_withdrawal_rate=4,
        max_years=30,
    )

    assert result["initial_fi_target"] == pytest.approx(6_000_000)  # FI target
    assert result["years_to_fi"] is None  # FI is not achievable under these conditions
    assert result["monthly_savings_rate"] == pytest.approx(50.0)  # 50% savings rate
