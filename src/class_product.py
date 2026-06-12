from abc import ABC, abstractmethod
from typing import Any


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление продукта."""
        pass

    @abstractmethod
    def __add__(self, other: 'BaseProduct') -> float:
        """Сложение продуктов."""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Геттер для цены."""
        pass


class PrintMixin:
    """Миксин для вывода информации о создании объекта."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Выводит информацию о создании объекта."""
        # Формируем строку с аргументами для вывода
        if args:
            args_str = ', '.join(repr(arg) for arg in args)
            print(f"{self.__class__.__name__}({args_str})")
        # НЕ вызываем super().__init__() здесь, чтобы избежать проблем с object


class Product(BaseProduct, PrintMixin):
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = float(price)
        self.quantity = quantity
        # Вызываем миксин явно
        PrintMixin.__init__(self, name, description, price, quantity)

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер для цены с проверкой."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if value < self.__price:
            user_input = input(f"Цена понижается с {self.__price} до {value}. Вы согласны? (y/n): ")
            if user_input.lower() == 'y':
                self.__price = value
                print(f"Цена изменена на {value}")
            else:
                print("Операция отменена")
        else:
            self.__price = value
            print(f"Цена изменена на {value}")

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """Магический метод сложения двух продуктов."""
        if not isinstance(other, BaseProduct):
            raise TypeError(f"Невозможно сложить Product с {type(other).__name__}")
        if type(self) != type(other):
            raise TypeError(f"Невозможно сложить товары разных классов: "
                           f"{type(self).__name__} и {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None) -> 'Product':
        """Класс-метод для создания продукта из словаря."""
        name = product_data.get("name")
        description = product_data.get("description")
        price = float(product_data.get("price"))
        quantity = product_data.get("quantity", 0)

        if existing_products is not None:
            for existing_product in existing_products:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    print(f"Товар '{name}' уже существует. Количество обновлено до "
                          f"{existing_product.quantity}")
                    return existing_product

        return cls(name, description, price, quantity)


class Smartphone(Product):
    """Класс, представляющий смартфон. Наследник класса Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        """Строковое представление смартфона."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


class LawnGrass(Product):
    """Класс, представляющий газонную траву. Наследник класса Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        """Строковое представление газонной травы."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."
