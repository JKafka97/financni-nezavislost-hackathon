import math


average_inflation = 0.02
average_interest = 0.03


#user inputs
monthly_amount_to_invest = 300
monthly_average_expenses = 700
savings = 0
target_capital = (monthly_average_expenses*12)/0.04
n = 12


def years_to_financial_independence(savings):
    t = math.log((target_capital * average_interest / n + monthly_amount_to_invest)
                / (savings * average_interest / n + monthly_amount_to_invest)) \
        / (n * math.log(1 + average_interest / n))
    return t

years = years_to_financial_independence(savings)
print(f"Time required: {years:.2f} years")

earning_by_years = [savings]

for year in range(1):
    pass