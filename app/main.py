import streamlit as st
import pandas as pd
from calculation import calculate_fi_metrics
from visual import plot_investment
from utils import format_currency, format_time

# Configure the page title and layout
st.set_page_config(page_title="Path to Financial FREEDOM!", layout="wide")

# Main header
st.markdown(
    "<h2 style='text-align: center;'>Path to Financial FREEDOM! 💰</h2>",
    unsafe_allow_html=True,
)

# Input section for user data
col1 = st.columns(1)[0]
with col1:
    st.subheader("Vaše údaje ✏️")
    monthly_savings = st.number_input(
        "Volná částka na investice (CZK)", value=30000, step=1000
    )
    monthly_expenses = st.number_input("Měsíční náklady (CZK)", value=50000, step=1000)
    current_savings = st.number_input("Úspory (CZK)", value=600000, step=10000)

# Advanced settings section
st.subheader("Pokročilé nastavení 🔧")
with st.expander("Upravit předpoklady výpočtu"):
    col_adv1, col_adv2, col_adv3 = st.columns(3)
    with col_adv1:
        investment_return = st.slider("Očekávaný výnos (%)", 1, 15, 8)
    with col_adv2:
        inflation_rate = st.slider("Očekávaná inflace (%)", 1, 10, 3)
    with col_adv3:
        safe_withdrawal_rate = st.slider("Výběr úroků (%)", 1, 10, 4)

    st.info("💡 These values affect your path to financial independence...")

# Calculate financial independence metrics
metrics = calculate_fi_metrics(
    monthly_savings,
    monthly_expenses,
    current_savings,
    investment_return,
    inflation_rate,
    safe_withdrawal_rate,
)

# Results section with key metrics
st.subheader("Výsledky")
col3, col4, col5 = st.columns(3)
with col3:
    st.metric(
        "Počáteční cíl finanční nezávislosti",
        format_currency(metrics["initial_fi_target"]),
    )
with col4:
    if metrics["years_to_fi"]:
        st.metric("Čas k finanční nezávislosti", format_time(metrics["years_to_fi"]))
    else:
        st.metric("Čas do finanční nezávislosti", "Více než 50 let")
with col5:
    st.metric("Měsíční míra úspor", f"{metrics['monthly_savings_rate']:.1f} %")

# Display investment chart
st.plotly_chart(
    plot_investment(metrics["fire_data"], metrics["years_to_fi"]),
    use_container_width=True,
)

# Milestones Analysis
st.subheader("Analýza milníků")
if metrics["years_to_fi"]:
    milestones = pd.DataFrame(
        {
            "Milníky finanční nezávislosti (%)": [25, 50, 75, 100],
            "Čas": [
                metrics["years_to_fi"] * 0.25,
                metrics["years_to_fi"] * 0.5,
                metrics["years_to_fi"] * 0.75,
                metrics["years_to_fi"],
            ],
        }
    )
    milestones["Čas"] = milestones["Čas"].apply(format_time)
    st.dataframe(milestones, hide_index=True)

st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px 0;'>
        © 2024 Path to Financial FREEDOM! All rights reserved.
        <br>Created with ❤️ by ušetřené==vydělané
    </div>
    """,
    unsafe_allow_html=True,
)
