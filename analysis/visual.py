import plotly.graph_objects as go
import plotly
import numpy as np
import pandas as pd

year_of_independance = 2040
initial_investment = 10000  # Starting with $10,000
mean_return = 0.08  # 8% average annual return
volatility = 0.15  # 15% volatility
years = 30  # Simulating for 30 years

def simulate_data(initial_value, num_of_years, mean_return, volatility):

    investment_values = [initial_value]
    # annual_returns = np.random.normal(loc=mean_return, scale=volatility, size=num_of_years)

    for _ in range(num_of_years):
        investment_values.append(investment_values[-1] * (1 + mean_return))

    years_range = np.arange(2024, 2024 + num_of_years + 1)
    df = pd.DataFrame({
        'year': years_range,
        'investment': investment_values
    })

    return df

def plot_investment(
        investment_data: pd.DataFrame,
        year_of_independance: int
        ) -> plotly.graph_objects.Figure:
    """
    This function creates a plotly line figure with investment data thru years.
    
    Parameters:
    investment_data (pd.DateFrame): Dataframe of investments thru years 
    year_of_independance: Year, when customer will achive financial independance
    
    Returns:
    plotly.figure: Plotly figure that can be displayed
    """
    # Iniciate figure
    fig = go.Figure()
    # Add line for investment
    fig.add_trace(
        go.Scatter(
            x=investment_data["year"],
            y=investment_data["investment"],
            name="Investiční portfolio",
            line=dict(color="#2ecc71"),
        )
    )
    # Update visuals
    fig.update_layout(
        title="Cesta k finanční NEZÁVISLOSTI!",
        xaxis_title="Roky",
        yaxis_title="Částka (CZK)",
        hovermode="x unified",
        showlegend=True,
        template="plotly_white"
    )
    # Creates dashed v line fro year_of_independance, if exists
    if year_of_independance:
        fig.add_vline(x=year_of_independance, 
            line_dash="dash",
            annotation_text="Rok nezávislosti!", 
            annotation_position="bottom right",
            line_color="red")

    return fig

investment_data = simulate_data(initial_investment,years, mean_return, volatility)
fig = plot_investment(investment_data, year_of_independance)
fig.show()