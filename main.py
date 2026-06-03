from src.class_category import Category
from src.class_product import Product
from src.from_jason import load_categories_from_json

# Товары
product1 = Product(
    "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
)
product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

if __name__ == "__main__":

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(category1.products)
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, "
        "станет вашим другом и помощником",
        [product4]
    )

    print(category2.name)
    print(category2.description)
    # Используем геттер products (возвращает строку)
    print(category2.products)

    products_list: list[Product] = category2.get_products_list()
    if products_list:
        print(products_list[0].name)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")

    # Тестируем add_product
    print("\n--- Тестирование add_product ---")
    product5 = Product("Xiaomi TV", "4K Smart TV", 45000.0, 10)
    category2.add_product(product5)
    print(f"После добавления товара в категорию '{category2.name}':")
    print(category2.products)
    print(f"Общее количество продуктов: {Category.product_count}")

    # Тестируем new_product (класс-метод)
    print("\n--- Тестирование new_product (класс-метод) ---")
    existing_products = [product1, product2, product3]

    new_product_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
    }

    created_product = Product.new_product(new_product_data, existing_products)
    print(f"Создан/обновлен продукт: {created_product.name}")
    print(f"  Количество: {created_product.quantity}")
    print(f"  Цена: {created_product.price}")

    # Создаем новый уникальный продукт
    new_unique_product = Product.new_product(
        {"name": "Google Pixel 8", "description": "128GB, Black", "price": 70000.0, "quantity": 15},
        existing_products
    )
    print(f"Создан новый продукт: {new_unique_product.name}")
    existing_products.append(new_unique_product)

    # Тестируем сеттер цены с проверками
    print("\n--- Тестирование сеттера цены (защита от некорректных значений) ---")
    test_product = Product("Test Phone", "For price testing", 50000.0, 1)
    print(f"Текущая цена: {test_product.price}")

    # Попытка установить отрицательную цену
    print("\nПопытка установить цену -100:")
    test_product.price = -100
    print(f"Цена после попытки: {test_product.price}")

    # Попытка установить нулевую цену
    print("\nПопытка установить цену 0:")
    test_product.price = 0
    print(f"Цена после попытки: {test_product.price}")

    # Корректное изменение цены
    print("\nКорректное изменение цены на 45000:")
    test_product.price = 45000
    print(f"Цена после изменения: {test_product.price}")

    # Дополнительное задание: подтверждение при понижении цены
    print("\n--- Дополнительное задание: подтверждение при понижении цены ---")
    print("Сейчас будет запрос на подтверждение понижения цены.")
    print("Текущая цена: 45000")
    print("Попытка понизить до 40000:")
    test_product.price = 40000  # Здесь потребуется ввод y/n
    print(f"Итоговая цена: {test_product.price}")

    # ========== ЗАГРУЗКА ИЗ JSON (дополнительное задание) ==========
    print("\n" + "=" * 60)
    print("ЧАСТЬ 3: ЗАГРУЗКА КАТЕГОРИЙ ИЗ JSON")
    print("=" * 60)

    try:
        categories = load_categories_from_json('data/products.json')
        print("\nКатегории и продукты из внешнего файла:")
        for cat in categories:
            print(f"Категория: {cat.name}, товаров: {len(cat.get_products_list())}")
            print(f"  Товары: {cat.products}")
    except FileNotFoundError:
        print("Файл data/products.json не найден. Пропускаем загрузку из JSON.")
    except Exception as e:
        print(f"Ошибка при загрузке JSON: {e}")

    # Итоговая информация
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ ИНФОРМАЦИЯ")
    print("=" * 60)
    print(f"Всего создано категорий: {Category.category_count}")
    print(f"Всего продуктов (суммарно по всем категориям): {Category.product_count}")
