import plotly.graph_objects as go
import plotly
import pandas as pd

def plot_investment(
        investment_data: pd.DataFrame,
        year_to_independance: int
        ) -> plotly.graph_objects.Figure:
    """
    This function creates a plotly line figure with investment data thru years.
    
    Parameters:
    investment_data (pd.DateFrame): Dataframe of investments thru years 
    year_to_independance: Years, when customer will achive financial independance
    
    Returns:
    plotly.figure: Plotly figure that can be displayed
    """
    # Iniciate figure
    fig = go.Figure()

    # Add current year to years
    investment_data["years"] = investment_data["years"] + 2024

    # Format values for hoverover values
    formatted_port = [f"{val:,.0f}".replace(",", " ") for val in investment_data["portfolio_real"]]
    formatted_fi = [f"{val:,.0f}".replace(",", " ") for val in investment_data["fi_target"]]
    # Add line for investment
    fig.add_trace(
        go.Scatter(
            x=investment_data["years"],
            y=investment_data["portfolio_real"],
            name="Investiční portfolio",
            line=dict(color="#2ecc71"),
            hovertemplate="Investice: %{customdata} CZK" + "<extra></extra>",
            customdata=formatted_port
        )
    )
    # Add trace line for FI target
    fig.add_trace(
        go.Scatter(
            x=investment_data["years"],
            y=investment_data["fi_target"],
            name="FN Cíl",
            line=dict(color="red"),
            hovertemplate="FI Cíl: %{customdata} CZK" + "<extra></extra>",
            customdata=formatted_fi
        )
    )
    # Update visuals
    fig.update_layout(
        title="Cesta k finanční NEZÁVISLOSTI!",
        xaxis_title="Roky",
        yaxis_title="Částka (CZK)",
        hovermode="x unified",
        showlegend=True,
        template="plotly_white",
        xaxis_tickformat = '.0f',
        legend=dict(
            font=dict(
                size=20, 
            )
        ),
        hoverlabel=dict(
            font=dict(
                size=16,
            )
        )
    )
    # Creates dashed v line for year_to_independance, if exists
    if year_to_independance:
        year_to_independance = year_to_independance + investment_data["years"].min()
        fig.add_vline(x=year_to_independance, 
            line_dash="dash",
            annotation_text=f"Rok nezávislosti!({year_to_independance:,.0f})".replace(',',''), 
            annotation_position="bottom right",
            line_color="red",
            annotation_font=dict(
                size=20
            )
            )

    return fig
