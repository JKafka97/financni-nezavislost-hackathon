import plotly.graph_objects as go
import pandas as pd
from app.fi_visual import plot_investment


################################################################################################
def test_plot_investment_trace_count():
    sample_investment_data = pd.DataFrame(
        {
            "years": [0, 1, 2, 3, 4],
            "portfolio_real": [100000, 120000, 150000, 180000, 220000],
            "fi_target": [150000, 160000, 170000, 180000, 190000],
        }
    )
    # Test the number of traces created
    fig = plot_investment(sample_investment_data, year_to_independence=3)
    assert (
        len(fig.data) == 2
    )  # Should have 2 traces: one for the portfolio and one for the FI target


def test_plot_investment_titles():
    sample_investment_data = pd.DataFrame(
        {
            "years": [0, 1, 2, 3, 4],
            "portfolio_real": [100000, 120000, 150000, 180000, 220000],
            "fi_target": [150000, 160000, 170000, 180000, 190000],
        }
    )
    fig = plot_investment(sample_investment_data, year_to_independence=0)
    layout = fig.layout
    assert "Cesta k finanční NEZÁVISLOSTI!" in str(
        layout.title
    )  # Check if the title is correct
    assert "Roky" in str(layout.xaxis.title)  # Check if the x-axis title is correct
    assert "Částka (CZK)" in str(
        layout.yaxis.title
    )  # Check if the y-axis title is correct


def test_plot_investment_is_figure():
    sample_investment_data = pd.DataFrame(
        {
            "years": [0, 1, 2, 3, 4],
            "portfolio_real": [100000, 120000, 150000, 180000, 220000],
            "fi_target": [150000, 160000, 170000, 180000, 190000],
        }
    )
    fig = plot_investment(sample_investment_data, year_to_independence=0)
    assert isinstance(fig, go.Figure)


################################################################################################
