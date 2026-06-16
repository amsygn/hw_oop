from typing import List
from abc import ABC, abstractmethod
from src.class_product import Product, ZeroQuantityError


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
        """
        Метод для добавления продукта в категорию.
        С обработкой исключений для нулевого количества.
        """
        try:
            # Сначала проверяем, является ли объект продуктом (Задание 3)
            if not isinstance(product, Product):
                raise TypeError(
                    f"Можно добавлять только объекты класса Product или его наследников. "
                    f"Получен {type(product).__name__}"
                )

            # Затем проверяем количество (Дополнительное задание)
            if product.quantity <= 0:
                raise ZeroQuantityError(
                    "Товар с нулевым количеством не может быть добавлен в категорию"
                )

            self.__products.append(product)
            Category.product_count += 1
            print(f"Товар '{product.name}' успешно добавлен в категорию")

        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            raise
        except TypeError as e:
            print(f"Ошибка типа: {e}")
            raise
        finally:
            print("Обработка добавления товара завершена")

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

    def middle_price(self) -> float:
        """
        Задание 2: подсчет среднего ценника всех товаров в категории.
        Если в категории нет товаров, возвращает 0.
        """
        try:
            if len(self.__products) == 0:
                return 0.0
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0.0


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
    """Класс, представляющий заказ."""

    def __init__(self, product: Product, quantity: int) -> None:
        try:
            if quantity <= 0:
                raise ZeroQuantityError("Количество товара в заказе должно быть положительным")
            if quantity > product.quantity:
                raise ValueError(f"Недостаточно товара на складе. Доступно: {product.quantity}")

            self.product = product
            self.quantity = quantity
            self.total_price = product.price * quantity
            print(f"Заказ на товар '{product.name}' в количестве {quantity} шт. успешно создан")

        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            raise
        finally:
            print("Обработка создания заказа завершена")

    def get_products_list(self) -> List[Product]:
        """Возвращает список продуктов в заказе."""
        return [self.product]

    def __str__(self) -> str:
        """Строковое представление заказа."""
        price_str = str(int(self.total_price)) if self.total_price == int(self.total_price) \
            else str(self.total_price)
        return f"Заказ: {self.product.name}, {self.quantity} шт., итого: {price_str} руб."
