#import libraries
import pytest
import plotly.graph_objects as go
import pandas as pd

#tested functions
from calculation import calculate_fi_number
from calculation import calculate_fi_metrics
from visual import plot_investment


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
    assert metrics['initial_fi_target'] == 15000000
    assert metrics['years_to_fi'] is None
    assert isinstance(metrics['fire_data'], pd.DataFrame)
    assert metrics['monthly_savings_rate'] > 0


def test_calculate_fi_metrics_high_investment_return():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=50000,
        current_savings=600000,
        investment_return=20,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics['years_to_fi'] < 20

def test_calculate_fi_metrics_zero_expenses():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=0,
        current_savings=600000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics['years_to_fi'] == 0

def test_calculate_fi_metrics_high_expenses():
    metrics = calculate_fi_metrics(
        monthly_savings=30000,
        monthly_expenses=100000,
        current_savings=600000,
        investment_return=7,
        inflation_rate=3,
        safe_withdrawal_rate=4,
    )
    assert metrics['years_to_fi'] is None
################################################################################################


################################################################################################
def test_plot_investment_trace_count():
    sample_investment_data = pd.DataFrame({
        "years": [0, 1, 2, 3, 4],
        "portfolio_real": [100000, 120000, 150000, 180000, 220000],
        "fi_target": [150000, 160000, 170000, 180000, 190000],
    })
    # Test the number of traces created
    fig = plot_investment(sample_investment_data, year_to_independance=3)
    assert len(fig.data) == 2  # Should have 2 traces: one for the portfolio and one for the FI target

def test_plot_investment_titles():
    sample_investment_data = pd.DataFrame({
        "years": [0, 1, 2, 3, 4],
        "portfolio_real": [100000, 120000, 150000, 180000, 220000],
        "fi_target": [150000, 160000, 170000, 180000, 190000],
    })
    fig = plot_investment(sample_investment_data, year_to_independance=None)
    layout = fig.layout
    assert layout.title == "Cesta k finanční NEZÁVISLOSTI!"  # Check if the title is correct
    assert layout.xaxis.title == "Roky"  # Check if the x-axis title is correct
    assert layout.yaxis.title == "Částka (CZK)"  # Check if the y-axis title is correct

def test_plot_investment_titles():
    sample_investment_data = pd.DataFrame({
        "years": [0, 1, 2, 3, 4],
        "portfolio_real": [100000, 120000, 150000, 180000, 220000],
        "fi_target": [150000, 160000, 170000, 180000, 190000],
    })
    fig = plot_investment(sample_investment_data, year_to_independance=None)
    layout = fig.layout
    assert isinstance(fig, go.Figure)
################################################################################################