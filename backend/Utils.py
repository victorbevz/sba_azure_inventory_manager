# utils.py

def apply_global_discount(products, percent):
    for p in products:
        p.apply_discount(percent)


def format_currency(value: float):
    return f"{value:.2f} PLN"