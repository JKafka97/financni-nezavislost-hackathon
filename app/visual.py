import plotly.graph_objects as go
import pandas as pd
import datetime


def plot_investment(
    investment_data: pd.DataFrame, year_to_independence: int
) -> go.Figure:
    # Initialize the figure
    fig = go.Figure()

    # Add the current year to the investment years
    curr_year = datetime.datetime.now().year
    investment_data["years"] = investment_data["years"] + curr_year

    # Format values for hover text
    investment_data["formatted_portfolio"] = investment_data["portfolio_real"].apply(
        lambda x: f"{x:,.0f}".replace(",", " ")
    )
    investment_data["formatted_fi_target"] = investment_data["fi_target"].apply(
        lambda x: f"{x:,.0f}".replace(",", " ")
    )

    # Add portfolio trace (investment growth)
    fig.add_trace(
        go.Scatter(
            x=investment_data["years"],
            y=investment_data["portfolio_real"],
            name="Investiční portfolio",
            line=dict(color="#2ecc71"),
            hovertemplate="Investice: %{customdata} CZK<extra></extra>",
            customdata=investment_data["formatted_portfolio"],
        )
    )

    # Add Financial Independence (FI) target trace
    fig.add_trace(
        go.Scatter(
            x=investment_data["years"],
            y=investment_data["fi_target"],
            name="FN Cíl",
            line=dict(color="red"),
            hovertemplate="FI Cíl: %{customdata} CZK<extra></extra>",
            customdata=investment_data["formatted_fi_target"],
        )
    )

    # Update layout for the figure
    fig.update_layout(
        title="Cesta k finanční NEZÁVISLOSTI!",
        xaxis_title="Roky",
        yaxis_title="Částka (CZK)",
        hovermode="x unified",
        showlegend=True,
        template="plotly_white",
        xaxis_tickformat=".0f",
        legend=dict(font=dict(size=20)),
        hoverlabel=dict(font=dict(size=16)),
    )

    # Add vertical dashed line for year of independence if specified
    if year_to_independence:
        independence_year = year_to_independence + investment_data["years"].min()
        fig.add_vline(
            x=independence_year,
            line_dash="dash",
            annotation_text=f"Rok nezávislosti! ({independence_year:,.0f})".replace(
                ",", ""
            ),
            annotation_position="bottom right",
            line_color="red",
            annotation_font=dict(size=20),
        )

    return fig
