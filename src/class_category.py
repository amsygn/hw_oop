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

        # Оптимизирован с использованием __str__ продукта
        result = []
        for product in self.__products:
            result.append(str(product))

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

    def __str__(self) -> str:
        """
        Строковое представление категории.
        Формат: "Название категории, количество продуктов: X шт."
        Где количество продуктов - суммарное количество всех товаров на складе в категории.
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """
        Возвращает итератор для перебора товаров категории.
        (Дополнительное задание)
        """
        return CategoryIterator(self)


class CategoryIterator:
    """
    Вспомогательный класс для итерации по товарам категории.
    (Дополнительное задание)
    """

    def __init__(self, category: Category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Product:
        if self._index < len(self._category.get_products_list()):
            product = self._category.get_products_list()[self._index]
            self._index += 1
            return product
        raise StopIteration
