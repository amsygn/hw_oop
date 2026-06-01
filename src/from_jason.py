import json

from typing import List

from main import Category, Product


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
