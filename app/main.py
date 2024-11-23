import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from calculation import calculate_fi_metrics
from visual import plot_investment

st.set_page_config(page_title="Path to Financial FREEDOM!", layout="wide")

st.markdown(
    """
    <h2 style="text-align: center;">Path to Financial FREEDOM! 💰</h2>
    """,
    unsafe_allow_html=True,
)

# Main inputs - using a single column to match the layout
col1 = st.columns(1)[0]

with col1:
    st.subheader("Vaše údaje ✏️")
    monthly_savings = st.number_input(
        "Volná částka na investice (CZK)", value=30000, step=1000
    )
    monthly_expenses = st.number_input("Měsíční náklady (CZK)", value=50000, step=1000)
    current_savings = st.number_input("Úspory (CZK)", value=600000, step=10000)

# Advanced settings header aligned with inputs
st.subheader("Pokročilé nastavení 🔧")

# Advanced options in expander
with st.expander("Upravit předpoklady výpočtu", expanded=False):
    col_adv1, col_adv2, col_adv3 = st.columns(3)

    with col_adv1:
        investment_return = st.slider("Očekávaný výnos (%)", 1, 15, 8)
    with col_adv2:
        inflation_rate = st.slider("Očekávaná inflace (%)", 1, 10, 3)
    with col_adv3:
        safe_withdrawal_rate = st.slider("Výběr úroků (%)", 1, 10, 4)

    st.info(
        """
        💡 Tyto hodnoty ovlivňují výpočet vaší cesty k finanční nezávislosti:
        - Očekávaný výnos: Průměrný roční výnos vašich investic
        - Očekávaná inflace: Předpokládaná míra růstu cen
        - Výběr úroků: Bezpečná míra ročního čerpání z portfolia
        """
    )

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
        f"{metrics['initial_fi_target']:,.0f} CZK".replace(",", " "),
    )

with col4:
    if metrics["years_to_fi"] is not None:
        years = int(metrics["years_to_fi"])
        months = int((metrics["years_to_fi"] - years) * 12)
        st.metric("Čas k finanční nezávislosti", f"{years}r {months}m")
    else:
        st.metric("Čas do finanční nezávislosti", "Více než 50 let")

with col5:
    st.metric("Měsíční míra úspor", f"{metrics['monthly_savings_rate']:.1f} %")

st.plotly_chart(
    plot_investment(metrics["fire_data"], metrics["years_to_fi"]),
    use_container_width=True,
)

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
            {
                "Milníky finanční nezávislosti (%)": f"{milestone*100:.0f}",
                "Čas": f"{years}r {months}m",
            }
        )

milestone_data = pd.DataFrame(milestone_data)

if not milestone_data.empty:
    st.dataframe(milestone_data, hide_index=True)

# Add Fin-gram link button after inputs
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <a href='https://fin-gram-cc79f963fdbc.herokuapp.com/' target='_blank'>
            <button style='
                background-color: #00395d;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 0;
                transition: all 0.3s ease;
            '>
                Finační poradce na klik 🤖
            </button>
        </a>
    </div>
    <style>
        button:hover {
            background-color: #00aeef !important;
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px 0;'>
        © 2024 Path to Financial FREEDOM! All rights reserved.
        <br>Created with ❤️ by ušetřené==vydělané
    </div>
    """,
    unsafe_allow_html=True,
)
