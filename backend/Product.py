# product.py
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return self.price * self.quantity

    def apply_discount(self, percent: float):
        self.price = self.price * (1 - percent / 100)

    def __str__(self):
        return f"{self.name}: {self.price:.2f} x {self.quantity}"