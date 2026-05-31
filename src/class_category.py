from typing import List


class Category:

    category_count: int = 0  # Общее количество категорий
    product_count: int = 0  # Общее количество товаров (уникальных продуктов)

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)

