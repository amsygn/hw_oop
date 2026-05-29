from main import Product, Category

product1 = Product("Продукт A", "Описание A", 100.0, 5)
product2 = Product("Продукт Б", "Описание Б", 200.0, 3)

# ТЕСТ 1: Корректность инициализации объектов класса Product
print("\n1. Тест инициализации Product:")
test_product = Product("Test Phone", "Test description", 999.99, 10)
assert test_product.name == "Test Phone", "Ошибка: name"
assert test_product.description == "Test description", "Ошибка: description"
assert test_product.price == 999.99, "Ошибка: price"
assert test_product.quantity == 10, "Ошибка: quantity"
print("Класс Product инициализирован корректно")

# ТЕСТ 2: Корректность инициализации объектов класса Category
print("\n2. Тест инициализации Category:")
test_category = Category("Electronics", "Devices", [product1, product2])
assert test_category.name == "Electronics", "Ошибка категории name"
assert test_category.description == "Devices", "Ошибка категории description"
assert len(test_category.products) == 2, "Ошибка в количестве продуктов"
assert test_category.products[0] == product1, "Ошибка: продукт А"
assert test_category.products[1] == product2, "Ошибка: продукт Б"
print(" Класс Category инициализирован корректно")

# ТЕСТ 3: Подсчет количества продуктов
print("\n3. Тест подсчета количества продуктов:")
Category.category_count = 0
Category.product_count = 0
Category("Категория A", "Описание A", [product1, product2])  # +2 продукта
Category("Категория Б", "Описание Б", [product1])             # +1 продукт
assert Category.product_count == 3, f"Ошибка: ожидалось 3, получено {Category.product_count}"
print(f"Количество продуктов: {Category.product_count} (ожидалось: 3)")

# ТЕСТ 4: Подсчет количества категорий
print("\n4. Тест подсчета количества категорий:")
Category.category_count = 0
Category.product_count = 0
Category("Cat1", "Desc1", [product1])  # +1 категория
Category("Cat2", "Desc2", [product2])  # +1 категория
Category("Cat3", "Desc3", [product1])  # +1 категория
assert Category.category_count == 3, f"Ошибка: ожидалось 3, получено {Category.category_count}"
print(f"Количество категорий: {Category.category_count} (ожидалось: 3)")
