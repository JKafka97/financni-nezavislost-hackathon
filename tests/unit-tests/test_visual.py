import pytest
import pandas as pd
import datetime
from app.visual import plot_investment
from plotly.graph_objects import Figure


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "years": [0, 1, 2],
            "portfolio_real": [100000, 200000, 300000],
            "fi_target": [500000, 500000, 500000],
        }
    )


def test_plot_investment_structure(sample_data):
    curr_year = datetime.datetime.now().year
    fig = plot_investment(sample_data.copy(), 5)

    assert isinstance(fig, Figure)

    assert len(fig.data) == 2
    assert fig.data[0].name == "Investiční portfolio"
    assert fig.data[1].name == "FN Cíl"

    expected_years = [curr_year, curr_year + 1, curr_year + 2]
    assert list(fig.data[0].x) == expected_years
    assert list(fig.data[1].x) == expected_years


def test_formatted_values(sample_data):
    fig = plot_investment(sample_data.copy(), 5)

    formatted_portfolio = ["100 000", "200 000", "300 000"]
    formatted_fi_target = ["500 000", "500 000", "500 000"]
    assert list(fig.data[0].customdata) == formatted_portfolio
    assert list(fig.data[1].customdata) == formatted_fi_target


def test_independence_year(sample_data):
    fig = plot_investment(sample_data.copy(), 5)

    annotations = [
        a.text for a in fig.layout.annotations if "Rok nezávislosti!" in a.text
    ]
    assert len(annotations) == 1

    independence_year = datetime.datetime.now().year + 5
    assert f"{independence_year:,}" in annotations[0]


def test_layout_settings(sample_data):
    fig = plot_investment(sample_data.copy(), 5)

    assert fig.layout.title.text == "Cesta k finanční NEZÁVISLOSTI!"
    assert fig.layout.xaxis.title.text == "Roky"
    assert fig.layout.yaxis.title.text == "Částka (CZK)"
    assert fig.layout.hovermode == "x unified"
