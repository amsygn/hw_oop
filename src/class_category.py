from typing import List
from abc import ABC, abstractmethod
from src.class_product import Product


class BaseCategory(ABC):
    """Абстрактный базовый класс для категорий и заказов."""

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление."""
        pass

    @abstractmethod
    def get_products_list(self) -> List:
        """Получение списка продуктов."""
        pass


class Category(BaseCategory):
    """Класс, представляющий категорию товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def products(self) -> str:
        """Геттер для вывода списка товаров в виде строки."""
        if not self.__products:
            return "В категории нет товаров"

        result = []
        for product in self.__products:
            result.append(str(product))

        return "\n".join(result)

    def add_product(self, product: Product) -> None:
        """Метод для добавления продукта в категорию."""
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты класса Product или его наследников."
                f"Получен {type(product).__name__}"
            )
        self.__products.append(product)
        Category.product_count += 1

    def get_products_list(self) -> List[Product]:
        """Метод для получения списка продуктов."""
        return self.__products

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Возвращает итератор для перебора товаров категории."""
        return CategoryIterator(self)


class CategoryIterator:
    """Вспомогательный класс для итерации по товарам категории."""

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


class Order(BaseCategory):
    """Класс, представляющий заказ (дополнительное задание)."""

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Количество товара должно быть положительным")
        if quantity > product.quantity:
            raise ValueError(f"Недостаточно товара на складе. Доступно: {product.quantity}")
        self.product = product
        self.quantity = quantity
        self.total_price = product.price * quantity

    def get_products_list(self) -> List[Product]:
        """Возвращает список продуктов в заказе."""
        return [self.product]

    def __str__(self) -> str:
        """Строковое представление заказа."""
        price_str = str(int(self.total_price)) if self.total_price == int(self.total_price) \
            else str(self.total_price)
        return f"Заказ: {self.product.name}, {self.quantity} шт., итого: {price_str} руб."
