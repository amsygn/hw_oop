class Product:
    """Класс, представляющий продукт."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self._price = float(price)  # Приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер для цены с проверкой."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительное задание: подтверждение при понижении цены
        if value < self._price:
            user_input = input(f"Цена понижается с {self._price} до {value}. Вы согласны? (y/n): ")
            if user_input.lower() == 'y':
                self._price = value
                print(f"Цена изменена на {value}")
            else:
                print("Операция отменена")
        else:
            self._price = value
            print(f"Цена изменена на {value}")

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
