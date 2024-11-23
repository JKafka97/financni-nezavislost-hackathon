import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def calculate_fi_number(monthly_expenses, safe_withdrawal_rate=4):
    annual_expenses = monthly_expenses * 12
    fi_number = (annual_expenses * 100) / safe_withdrawal_rate
    return fi_number


def calculate_fi_metrics(
    monthly_savings,
    monthly_expenses,
    current_savings,
    investment_return=7,
    inflation_rate=3,
    safe_withdrawal_rate=4,
):
    fi_number = calculate_fi_number(monthly_expenses, safe_withdrawal_rate)
    monthly_investment_return = (1 + investment_return / 100) ** (1 / 12) - 1
    monthly_inflation_rate = (1 + inflation_rate / 100) ** (1 / 12) - 1
    real_monthly_return = (1 + monthly_investment_return) / (
        1 + monthly_inflation_rate
    ) - 1

    max_years = 50
    years = np.linspace(0, max_years, max_years * 12 + 1)
    df = pd.DataFrame({"years": years})

    df["portfolio_nominal"] = [
        current_savings * (1 + monthly_investment_return) ** (i * 12)
        + monthly_savings
        * ((1 + monthly_investment_return) ** (i * 12) - 1)
        / monthly_investment_return
        for i in years
    ]

    df["portfolio_real"] = [
        current_savings * (1 + real_monthly_return) ** (i * 12)
        + monthly_savings
        * ((1 + real_monthly_return) ** (i * 12) - 1)
        / real_monthly_return
        for i in years
    ]

    df["expenses_annual"] = monthly_expenses * 12 * (1 + inflation_rate / 100) ** years
    df["fi_target"] = df["expenses_annual"] * (100 / safe_withdrawal_rate)

    fi_achieved_mask = df["portfolio_real"] >= df["fi_target"]
    years_to_fi = (
        df.loc[fi_achieved_mask, "years"].iloc[0] if fi_achieved_mask.any() else None
    )

    metrics = {
        "initial_fi_target": fi_number,
        "years_to_fi": years_to_fi,
        "portfolio_at_fi": (
            df.loc[fi_achieved_mask, "portfolio_real"].iloc[0] if years_to_fi else None
        ),
        "monthly_savings_rate": (monthly_savings / (monthly_savings + monthly_expenses))
        * 100,
        "fire_data": df,
    }
    return metrics


def create_timeline_plot(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["years"],
            y=df["portfolio_real"],
            name="Portfolio (Real)",
            line=dict(color="#2ecc71"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["years"],
            y=df["fi_target"],
            name="FI Target",
            line=dict(color="#e74c3c"),
        )
    )

    fig.update_layout(
        title="Path to Financial FREEDOM!",
        xaxis_title="Years",
        yaxis_title="Amount (CZK)",
        hovermode="x unified",
        showlegend=True,
    )
    return fig


st.set_page_config(page_title="Path to Financial FREEDOM!", layout="wide")

st.title("Path to Financial FREEDOM! 💰")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Vaše údaje")
    monthly_savings = st.number_input(
        "Volná částka na investice (CZK)", value=30000, step=1000
    )
    monthly_expenses = st.number_input("Měsíční náklady (CZK)", value=50000, step=1000)
    current_savings = st.number_input("Úspory (CZK)", value=600000, step=10000)

with col2:
    st.subheader("Předpoklady")
    investment_return = st.slider("Očekávaný výnos (%)", 1, 15, 8)
    inflation_rate = st.slider("Očekávaná inflace (%)", 1, 10, 3)
    safe_withdrawal_rate = st.slider("Výběr úroků (%)", 1, 10, 4)

metrics = calculate_fi_metrics(
    monthly_savings=monthly_savings,
    monthly_expenses=monthly_expenses,
    current_savings=current_savings,
    investment_return=investment_return,
    inflation_rate=inflation_rate,
    safe_withdrawal_rate=safe_withdrawal_rate,
)

st.subheader("Výsledky")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric(
        "Počáteční cíl finanční nezávislosti",
        f"{metrics['initial_fi_target']:,.0f} CZK",
    )

with col4:
    if metrics["years_to_fi"] is not None:
        years = int(metrics["years_to_fi"])
        months = int((metrics["years_to_fi"] - years) * 12)
        st.metric("Čas k finanční nezávislosti", f"{years}y {months}m")
    else:
        st.metric("Čas do finanční nezávislosti", "Více než 50 let")

with col5:
    st.metric("Měsíční míra úspor", f"{metrics['monthly_savings_rate']:.1f}%")

st.plotly_chart(create_timeline_plot(metrics["fire_data"]), use_container_width=True)

st.subheader("Analýza milníků")
milestones = [0.25, 0.5, 0.75, 1.0]
initial_target = metrics["initial_fi_target"]
fire_data = metrics["fire_data"]

milestone_data = []
for milestone in milestones:
    milestone_mask = fire_data["portfolio_real"] >= (initial_target * milestone)
    if milestone_mask.any():
        years_to_milestone = fire_data.loc[milestone_mask, "years"].iloc[0]
        years = int(years_to_milestone)
        months = int((years_to_milestone - years) * 12)
        milestone_data.append(
            {"Milníky": f"{milestone*100:.0f}% FI", "Čas": f"{years}y {months}m"}
        )

st.table(pd.DataFrame(milestone_data))

# Add Fin-gram link button after inputs
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <a href='https://fin-gram-cc79f963fdbc.herokuapp.com/' target='_blank'>
            <button style='
                background-color: #00aeef;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 0;
            '>
                Finační poradce na klik 🤖
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")
