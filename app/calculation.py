import numpy as np
import pandas as pd


def calculate_fi_number(monthly_expenses, safe_withdrawal_rate=4):
    annual_expenses = monthly_expenses * 12
    return annual_expenses * 100 / safe_withdrawal_rate


def calculate_fi_metrics(
    monthly_savings,
    monthly_expenses,
    current_savings,
    investment_return=7,
    inflation_rate=3,
    safe_withdrawal_rate=4,
    max_years=50,
):
    fi_target_initial = calculate_fi_number(monthly_expenses, safe_withdrawal_rate)

    monthly_investment_return = (1 + investment_return / 100) ** (1 / 12) - 1
    monthly_inflation_rate = (1 + inflation_rate / 100) ** (1 / 12) - 1

    real_monthly_return = (1 + monthly_investment_return) / (
        1 + monthly_inflation_rate
    ) - 1
    real_monthly_return = max(real_monthly_return, 1e-10)

    years = np.linspace(0, max_years, max_years * 12 + 1)
    df = pd.DataFrame({"years": years})

    df["portfolio_nominal"] = np.array(
        [
            current_savings * (1 + monthly_investment_return) ** (i * 12)
            + monthly_savings
            * ((1 + monthly_investment_return) ** (i * 12) - 1)
            / monthly_investment_return
            for i in years
        ]
    )

    df["portfolio_real"] = np.array(
        [
            current_savings * (1 + real_monthly_return) ** (i * 12)
            + monthly_savings
            * ((1 + real_monthly_return) ** (i * 12) - 1)
            / real_monthly_return
            for i in years
        ]
    )

    df["expenses_annual"] = monthly_expenses * 12 * (1 + inflation_rate / 100) ** years
    df["fi_target"] = df["expenses_annual"] * (100 / safe_withdrawal_rate)

    fi_achieved_mask = df["portfolio_real"] >= df["fi_target"]
    years_to_fi = (
        df.loc[fi_achieved_mask, "years"].iloc[0] if fi_achieved_mask.any() else None
    )

    return {
        "initial_fi_target": fi_target_initial,
        "years_to_fi": years_to_fi,
        "monthly_savings_rate": (monthly_savings / (monthly_savings + monthly_expenses))
        * 100,
        "fire_data": df,
    }
