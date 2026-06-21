import unittest
from Product import Product
from Inventory import Inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.add_product(Product("Test", 100, 5))

    def test_total_value(self):
        # Проверяем базу: 100 * 5 = 500
        self.assertEqual(self.inv.total_inventory_value(), 500)

    def test_remove(self):
        # Проверяем твою новую функцию удаления
        self.inv.remove_product("Test")
        self.assertEqual(len(self.inv.products), 0)

    def test_low_stock(self):
        # Проверяем поиск остатков
        low = self.inv.get_low_stock(10)
        self.assertEqual(len(low), 1)