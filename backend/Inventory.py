# inventory.py

from Product import Product

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, name: str):
        # Удаление товара (Роль Б добавила это)
        self.products = [p for p in self.products if p.name.lower() != name.lower()]

    def get_low_stock(self, threshold: int):
        # Поиск товаров, которых мало на складе
        return [p for p in self.products if p.quantity < threshold]

    def total_inventory_value(self):
        return sum(p.total_value() for p in self.products)

    def show_all(self):
        for p in self.products:
            print(p)

    def find_product(self, name: str):
        for p in self.products:
            if p.name.lower() == name.lower():
                return p
        return None