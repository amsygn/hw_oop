from typing import List
from src.class_product import Product


class Category:
    """Класс, представляющий категорию товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def products(self) -> str:
        """
        Геттер для вывода списка товаров в виде строки.
        Формат: "Название продукта, X руб. Остаток: Y шт."
        """
        if not self.__products:
            return "В категории нет товаров"

        result = []
        for product in self.__products:
            result.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")

        return "\n".join(result)

    def add_product(self, product: Product) -> None:
        """Метод для добавления продукта в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    def get_products_list(self) -> List[Product]:
        """
        Метод для получения списка продуктов (для обратной совместимости и тестов).
        Возвращает список объектов Product.
        """
        return self.__products
