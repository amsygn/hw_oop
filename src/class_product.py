class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = float(price)  # Приватный атрибут цены
        self.quantity = quantity

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
        """
        Строковое представление продукта.
        Формат: "Название продукта, X руб. Остаток: X шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """
        Магический метод сложения двух продуктов.
        Возвращает сумму произведений цены на количество.
        """
        if not isinstance(other, Product):
            raise TypeError(f"Невозможно сложить Product с {type(other).__name__}")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None) -> 'Product':
        """
        Класс-метод для создания продукта из словаря.

        Дополнительное задание: проверка наличия товара с таким же именем.
        Если товар существует, складывает количество и выбирает максимальную цену.
        """
        name = product_data.get("name")
        description = product_data.get("description")
        price = float(product_data.get("price"))
        quantity = product_data.get("quantity", 0)

        # Проверка дубликатов
        if existing_products is not None:
            for existing_product in existing_products:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    print(f"Товар '{name}' уже существует. Количество обновлено до "
                          f"{existing_product.quantity}")
                    return existing_product

        # Создаем новый продукт
        return cls(name, description, price, quantity)
