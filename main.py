import json
from typing import List


class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = quantity


class Category:

    category_count: int = 0  # Общее количество категорий
    product_count: int = 0  # Общее количество товаров (уникальных продуктов)

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


# Товары из задания
product1 = Product(
    "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
)
product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


def load_categories_from_json(file_path: str) -> List[Category]:
    """Доп.задание: загружает данные из JSON файла и создает объекты Category и Product."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories: list[Category] = []

    for category_data in data:
        products = []
        for product_data in category_data.get('products', []):
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product)

        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == "__main__":

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения "
                         "дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, "
                         "станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products[0].name)

    print(Category.category_count)
    print(Category.product_count)

    # Пример загрузки из JSON
    categories = load_categories_from_json('data/products.json')
    print("\nКатегории и продукты из внешнего файла:")
    for cat in categories:
        print(f"Категория: {cat.name}, товаров: {len(cat.products)}")
