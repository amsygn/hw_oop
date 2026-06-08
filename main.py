from src.class_category import Category
from src.class_product import Product, Smartphone, LawnGrass
from src.from_jason import load_categories_from_json

if __name__ == '__main__':
    # Товары
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Демонстрация __str__ для продуктов
    print("••• Товары •••")
    print(str(product1))
    print(str(product2))
    print(str(product3))
    print()

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных "
        "функций для удобства жизни",
        [product1, product2, product3]
    )

    # Демонстрация __str__ для категории
    print("••• Категория •••")
    print(str(category1))
    print()

    # Демонстрация геттера products (использует __str__ продуктов)
    print("••• Список товаров в категории •••")
    print(category1.products)
    print()

    # Демонстрация __add__ для продуктов
    print("••• Общая стоимость товаров на складе •••")
    print(f"{product1.name} + {product2.name} = {product1 + product2}")
    print(f"{product1.name} + {product3.name} = {product1 + product3}")
    print(f"{product2.name} + {product3.name} = {product2 + product3}")
    print()

    print("••• Общая информация о категории •••")
    print(f'Категория:', category1.name)
    print(f'Описание:', category1.description)
    print(f'Товары в наличии:', category1.products)
    print(f'Кол-во категорий:', category1.category_count)
    print(f'Кол-во товаров:', category1.product_count)
    print()

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, "
                         "станет вашим другом и помощником",
                         [product4])

    print("••• Новая категория •••")
    print(f'Категория:', category2.name)
    print(f'Описание:', category2.description)
    print(f'Товары в наличии:', category2.products)
    print()

    products_list = category2.get_products_list()
    if products_list:
        print(f'Товары в наличии:', products_list[0].name)

    print(f'Всего категорий: ', Category.category_count)
    print(f'Всего товаров в наличии:', Category.product_count)

    # Демонстрация новых классов-наследников (Задание 1)
    print("\n" + "="*50)
    print("••• Демонстрация новых классов-наследников •••")
    print("="*50)

    # Создание смартфонов
    smartphone1 = Smartphone(
        "Xiaomi 13 Pro", "Флагманский смартфон", 89990.0, 15,
        "высокая", "13 Pro", 512, "черный"
    )
    smartphone2 = Smartphone(
        "Samsung Galaxy S24", "Новый флагман", 99990.0, 10,
        "максимальная", "S24", 256, "фиолетовый"
    )

    # Создание газонной травы
    grass1 = LawnGrass(
        "Газон 'Изумруд'", "Спортивный газон", 1500.0, 50,
        "Россия", 14, "зеленый"
    )
    grass2 = LawnGrass(
        "Газон 'Мавританский'", "Цветущий газон", 2000.0, 30,
        "Германия", 21, "разноцветный"
    )

    print("\n--- Смартфоны ---")
    print(str(smartphone1))
    print(str(smartphone2))

    print("\n--- Газонная трава ---")
    print(str(grass1))
    print(str(grass2))

    # Демонстрация сложения (Задание 2)
    print("\n••• Сложение товаров одного класса •••")
    print(f"Смартфон + Смартфон = {smartphone1 + smartphone2}")
    print(f"Трава + Трава = {grass1 + grass2}")

    print("\n••• Попытка сложения товаров разных классов •••")
    try:
        result = smartphone1 + grass1
        print(f"Результат: {result}")
    except TypeError as e:
        print(f"Ошибка (ожидаемо): {e}")

    # Демонстрация добавления в категории (Задание 3)
    print("\n••• Добавление товаров в категории •••")
    electronics_category = Category("Электроника", "Различные электронные устройства", [])

    electronics_category.add_product(smartphone1)
    electronics_category.add_product(smartphone2)
    electronics_category.add_product(product1)  # Обычный продукт тоже можно добавить

    print("Товары в категории 'Электроника':")
    print(electronics_category.products)

    garden_category = Category("Сад и огород", "Товары для сада", [])
    garden_category.add_product(grass1)
    garden_category.add_product(grass2)

    print("\nТовары в категории 'Сад и огород':")
    print(garden_category.products)

    print("\n••• Попытка добавить объект неправильного типа •••")
    try:
        electronics_category.add_product("это строка, а не продукт")
    except TypeError as e:
        print(f"Ошибка (ожидаемо): {e}")

    # Загрузка из JSON
    categories = load_categories_from_json('data/products.json')
    print("\nКатегории и продукты из внешнего файла:")
    for cat in categories:
        print(f"Категория: {cat.name}, товаров: {len(cat.get_products_list())}")

    # Демонстрация итератора
    print("\n••• Итерация по товарам категории (дополнительное задание) •••")
    for product in category1:
        print(f"  {product}")
