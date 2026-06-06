from src.class_category import Category
from src.class_product import Product
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

    # Загрузка из JSON (дополнительное задание)
    categories = load_categories_from_json('data/products.json')
    print("\nКатегории и продукты из внешнего файла:")
    for cat in categories:
        print(f"Категория: {cat.name}, товаров: {len(cat.get_products_list())}")

    # Демонстрация итератора (дополнительное задание)
    print("\n••• Итерация по товарам категории (дополнительное задание) •••")
    for product in category1:
        print(f"  {product}")
