import numpy as np
import pandas as pd


# Function to calculate the Financial Independence (FI) target number based on expenses and withdrawal rate
def calculate_fi_number(monthly_expenses, safe_withdrawal_rate=4):
    annual_expenses = monthly_expenses * 12
    fi_number = annual_expenses * 100 / safe_withdrawal_rate
    return fi_number


# Function to calculate FI metrics (e.g., when the FI target will be reached)
def calculate_fi_metrics(
    monthly_savings,
    monthly_expenses,
    current_savings,
    investment_return=7,
    inflation_rate=3,
    safe_withdrawal_rate=4,
    max_years=50,
):
    # Step 1: Calculate the initial FI target
    fi_target_initial = calculate_fi_number(monthly_expenses, safe_withdrawal_rate)

    # Step 2: Convert annual rates to monthly rates
    monthly_investment_return = (1 + investment_return / 100) ** (1 / 12) - 1
    monthly_inflation_rate = (1 + inflation_rate / 100) ** (1 / 12) - 1

    # Step 3: Adjust the investment return for inflation (real return)
    real_monthly_return = (1 + monthly_investment_return) / (
        1 + monthly_inflation_rate
    ) - 1
    real_monthly_return = (
        real_monthly_return if real_monthly_return != 0 else 1e-10
    )  # Prevent division by zero

    # Step 4: Define the years for simulation (monthly data over the range of max_years)
    years = np.linspace(0, max_years, max_years * 12 + 1)

    # Step 5: Initialize DataFrame to track projections
    df = pd.DataFrame({"years": years})

    # Step 6: Compute portfolio values over time (both nominal and real values)
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

    # Step 7: Calculate adjusted future expenses (accounting for inflation)
    df["expenses_annual"] = monthly_expenses * 12 * (1 + inflation_rate / 100) ** years

    # Step 8: Calculate the FI target for each year based on the safe withdrawal rate
    df["fi_target"] = df["expenses_annual"] * (100 / safe_withdrawal_rate)

    # Step 9: Identify the first year when FI is achieved (portfolio >= FI target)
    fi_achieved_mask = df["portfolio_real"] >= df["fi_target"]
    years_to_fi = (
        df.loc[fi_achieved_mask, "years"].iloc[0] if fi_achieved_mask.any() else None
    )

    # Step 10: Prepare the result metrics
    metrics = {
        "initial_fi_target": fi_target_initial,
        "years_to_fi": years_to_fi,
        "portfolio_at_fi": df.loc[fi_achieved_mask, "portfolio_real"].iloc[0]
        if years_to_fi
        else None,
        "monthly_savings_rate": (monthly_savings / (monthly_savings + monthly_expenses))
        * 100,
        "fire_data": df,
    }

    return metrics
