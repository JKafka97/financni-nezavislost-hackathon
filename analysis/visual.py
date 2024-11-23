import plotly.express as px
import plotly
import numpy as np
import pandas as pd

def simulate_data(initial_value, num_of_years, mean_return, volatility):

    investment_values = [initial_value]
    annual_returns = np.random.normal(loc=mean_return, scale=volatility, size=num_of_years)

    for year in range(num_of_years):
        investment_values.append(investment_values[-1] * (1 + mean_return))

    years_range = np.arange(2024, 2024 + num_of_years + 1)
    df = pd.DataFrame({
        'year': years_range,
        'investment': investment_values
    })

    return df

initial_investment = 10000  # Starting with $10,000
mean_return = 0.08  # 8% average annual return
volatility = 0.15  # 15% volatility
years = 30  # Simulating for 30 years

investment_data = simulate_data(initial_investment,years, mean_return, volatility)

year_of_independance = 2030

def plot_investment(
        investment_data: pd.DataFrame,
        year_of_independance: int
        ) -> plotly.graph_objects.Figure:

    fig = px.line(investment_data, x='year', y='investment',
                template='plotly_white')
    
    fig.update_xaxes(title_text='Years')
    fig.update_yaxes(title_text='Value of investment (CZK)')
    fig.add_vline(x=year_of_independance, 
                  line_width=3, 
                  line_dash="dash", 
                  line_color="red",
                  annotation_text=f"Independent in {year_of_independance}")

    return fig

fig = plot_investment(investment_data, year_of_independance)
fig.show()