import math


average_inflation = 0.02
average_interest = 0.03


#user inputs
monthly_amount_to_invest = 300
monthly_average_expenses = 700
savings_1 = 0
target_capital = (monthly_average_expenses*12)/0.04
n = 12


def years_to_financial_independence():
    if savings_1 == 0:
        t = math.log(1 + (target_capital * average_interest) 
                / (monthly_amount_to_invest * n)) / (n * math.log(1 + average_interest / n))
    elif savings_1 > 0:
        t = math.log((target_capital * average_interest / n + monthly_amount_to_invest)
                    / (savings_1 * average_interest / n + monthly_amount_to_invest)) \
            / (n * math.log(1 + average_interest / n))
    return t


print(f"Time required: {years_to_financial_independence():.2f} years")