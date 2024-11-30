def format_currency(value):
    return f"{value:,.0f} CZK".replace(",", " ")


def format_time(years):
    if years is None:
        return "Více než 50 let"
    years_int = int(years)
    total_months = round((years - years_int) * 12)
    if total_months == 12:
        years_int += 1
        total_months = 0
    return f"{years_int}r {total_months}m"
