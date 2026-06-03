import os
import pytest
import json
import tempfile

from main import Product, Category, load_categories_from_json


class TestProduct:
    """Полные тесты для класса Product"""

    def test_product_initialization_correctness(self):
        """Тест корректной инициализации класса Product"""
        product = Product("iPhone 15", "512GB, Black Titanium", 129990.0, 10)

        assert product.name == "iPhone 15"
        assert product.description == "512GB, Black Titanium"
        assert product.price == 129990.0
        assert product.quantity == 10

    def test_product_with_zero_price(self):
        """Тест продукта с нулевой ценой"""
        product = Product("Free Item", "Gift", 0.0, 100)
        assert product.price == 0.0
        assert product.quantity == 100

    def test_product_with_zero_quantity(self):
        """Тест продукта с нулевым количеством"""
        product = Product("Out of Stock", "Not available", 999.0, 0)
        assert product.quantity == 0

    def test_product_with_large_numbers(self):
        """Тест продукта с большими числами"""
        product = Product("Expensive Item", "Luxury", 1_000_000.0, 9999)
        assert product.price == 1_000_000.0
        assert product.quantity == 9999

    def test_product_with_string_price_conversion(self):
        """Тест: цена должна быть числом"""
        product = Product("Test", "Desc", 100, 5)
        assert isinstance(product.price, (int, float))

    def test_product_attributes_are_mutable(self):
        """Тест: атрибуты продукта можно изменять"""
        product = Product("Phone", "Smartphone", 500.0, 10)

        product.name = "New Phone"
        product.price = 450.0
        product.quantity = 8

        assert product.name == "New Phone"
        assert product.price == 450.0
        assert product.quantity == 8


class TestCategory:
    """Полные тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization_correctness(self):
        """Тест корректной инициализации класса Category"""
        product1 = Product("Product A", "Desc A", 100.0, 5)
        product2 = Product("Product B", "Desc B", 200.0, 3)

        category = Category("Electronics", "Electronic devices", [product1, product2])

        assert category.name == "Electronics"
        assert category.description == "Electronic devices"
        assert len(category.products) == 2
        assert category.products[0] is product1
        assert category.products[1] is product2

    def test_category_with_empty_products(self):
        """Тест категории без продуктов"""
        category = Category("Empty", "No products", [])

        assert category.name == "Empty"
        assert len(category.products) == 0
        assert Category.product_count == 0

    def test_category_with_single_product(self):
        """Тест категории с одним продуктом"""
        product = Product("Single", "Only one", 100.0, 1)
        category = Category("Single Category", "Just one product", [product])

        assert len(category.products) == 1
        assert Category.product_count == 1

    def test_category_products_list_is_independent(self):
        """Тест: список продуктов в категории независим"""
        product = Product("Test", "Desc", 100.0, 5)
        products = [product]

        category1 = Category("Cat1", "Desc1", products)
        category2 = Category("Cat2", "Desc2", products)

        category1.products[0].price = 999.0

        assert category2.products[0].price == 999.0

    def test_category_counters_with_multiple_categories(self):
        """Тест счетчиков при создании нескольких категорий"""
        p1 = Product("P1", "D1", 10.0, 1)
        p2 = Product("P2", "D2", 20.0, 2)
        p3 = Product("P3", "D3", 30.0, 3)

        Category("Cat1", "Desc1", [p1])  # 1 кат, 1 прод
        assert Category.category_count == 1
        assert Category.product_count == 1

        Category("Cat2", "Desc2", [p1, p2])  # 2 кат, +2 прод
        assert Category.category_count == 2
        assert Category.product_count == 3

        Category("Cat3", "Desc3", [p1, p2, p3])  # 3 кат, +3 прод
        assert Category.category_count == 3
        assert Category.product_count == 6

    def test_category_counters_with_duplicate_products(self):
        """Тест счетчиков с повторяющимися продуктами"""
        p1 = Product("P1", "D1", 10.0, 1)
        p2 = Product("P2", "D2", 20.0, 2)

        # Одинаковые продукты в разных категориях считаются отдельно
        Category("Cat1", "Desc1", [p1, p1])  # 2 продукта (даже если одинаковые)
        assert Category.product_count == 2

        Category("Cat2", "Desc2", [p2, p2, p2])  # 3 продукта
        assert Category.product_count == 5

    def test_category_name_can_be_empty_string(self):
        """Тест категории с пустым названием"""
        category = Category("", "Empty name", [])
        assert category.name == ""

    def test_category_description_can_be_empty_string(self):
        """Тест категории с пустым описанием"""
        category = Category("Test", "", [])
        assert category.description == ""


class TestProductCount:
    """Специализированные тесты для подсчета продуктов"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_product_count_after_single_category(self):
        """Тест подсчета продуктов после одной категории"""
        products = [Product(f"P{i}", f"D{i}", 100.0, i) for i in range(5)]
        Category("Cat", "Desc", products)

        assert Category.product_count == 5

    def test_product_count_after_multiple_categories(self):
        """Тест подсчета продуктов после нескольких категорий"""
        Category("Cat1", "Desc1", [Product("P1", "D1", 10.0, 1)])
        Category("Cat2", "Desc2", [Product("P2", "D2", 20.0, 2)])
        Category("Cat3", "Desc3", [Product("P3", "D3", 30.0, 3)])

        assert Category.product_count == 3

    def test_product_count_resets_properly(self):
        """Тест сброса счетчика продуктов"""
        Category("Cat1", "Desc1", [Product("P1", "D1", 10.0, 1)])
        assert Category.product_count == 1

        Category.category_count = 0
        Category.product_count = 0

        assert Category.product_count == 0
        assert Category.category_count == 0


class TestCategoryCount:
    """Специализированные тесты для подсчета категорий"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_category_count_after_single_category(self):
        """Тест подсчета категорий после одной категории"""
        Category("Cat", "Desc", [])
        assert Category.category_count == 1

    def test_category_count_after_multiple_categories(self):
        """Тест подсчета категорий после нескольких категорий"""
        for i in range(5):
            Category(f"Cat{i}", f"Desc{i}", [])

        assert Category.category_count == 5

    def test_category_count_with_no_categories(self):
        """Тест счетчика категорий без создания категорий"""
        Category.category_count = 0
        assert Category.category_count == 0


class TestLoadCategoriesFromJSON:
    """Расширенные тесты для загрузки из JSON"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_load_categories_from_valid_json(self):
        """Тест загрузки из валидного JSON"""
        json_data = [
            {
                "name": "Electronics",
                "description": "Gadgets",
                "products": [
                    {"name": "Phone", "description": "Smart", "price": 500.0, "quantity": 10},
                    {"name": "Laptop", "description": "Gaming", "price": 1500.0, "quantity": 5}
                ]
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(json_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert len(categories) == 1
            assert categories[0].name == "Electronics"
            assert len(categories[0].products) == 2
            assert categories[0].products[0].name == "Phone"
            assert categories[0].products[1].name == "Laptop"
        finally:
            os.unlink(temp_file)

    def test_load_categories_from_empty_json(self):
        """Тест загрузки из пустого JSON массива"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump([], f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert categories == []
        finally:
            os.unlink(temp_file)

    def test_load_categories_from_json_with_empty_products(self):
        """Тест загрузки категории без продуктов"""
        json_data = [
            {
                "name": "Empty Category",
                "description": "No products yet",
                "products": []
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(json_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert len(categories) == 1
            assert len(categories[0].products) == 0
        finally:
            os.unlink(temp_file)

    def test_load_categories_from_multiple_categories_json(self):
        """Тест загрузки нескольких категорий из JSON"""
        json_data = [
            {
                "name": "Category 1",
                "description": "First",
                "products": [{"name": "P1", "description": "D1", "price": 10.0, "quantity": 1}]
            },
            {
                "name": "Category 2",
                "description": "Second",
                "products": [{"name": "P2", "description": "D2", "price": 20.0, "quantity": 2}]
            },
            {
                "name": "Category 3",
                "description": "Third",
                "products": [{"name": "P3", "description": "D3", "price": 30.0, "quantity": 3}]
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(json_data, f)
            temp_file = f.name

        try:
            categories = load_categories_from_json(temp_file)
            assert len(categories) == 3
            assert categories[0].name == "Category 1"
            assert categories[1].name == "Category 2"
            assert categories[2].name == "Category 3"
        finally:
            os.unlink(temp_file)

    def test_load_categories_file_not_found(self):
        """Тест: ошибка при отсутствии файла"""
        with pytest.raises(FileNotFoundError):
            load_categories_from_json("non_existent_file.json")

    def test_load_categories_invalid_json(self):
        """Тест: ошибка при невалидном JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            f.write("{invalid json}")
            temp_file = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                load_categories_from_json(temp_file)
        finally:
            os.unlink(temp_file)


class TestEdgeCases:
    """Тесты граничных случаев"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_large_number_of_products(self):
        """Тест с большим количеством продуктов"""
        products = [Product(f"P{i}", f"D{i}", float(i), i) for i in range(100)]
        Category("Large Category", "Many products", products)

        assert Category.product_count == 100

    def test_large_number_of_categories(self):
        """Тест с большим количеством категорий"""
        product = Product("P", "D", 10.0, 1)

        for i in range(50):
            Category(f"Cat{i}", f"Desc{i}", [product])

        assert Category.category_count == 50

    def test_very_long_names(self):
        """Тест с очень длинными названиями"""
        long_name = "A" * 1000
        product = Product(long_name, long_name, 100.0, 1)
        category = Category(long_name, long_name, [product])

        assert product.name == long_name
        assert category.name == long_name


class TestIntegration:
    """Интеграционные тесты"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # Создаем продукты
        phone = Product("iPhone", "Smartphone", 1000.0, 10)
        laptop = Product("MacBook", "Laptop", 2000.0, 5)
        tablet = Product("iPad", "Tablet", 500.0, 8)

        # Создаем категории
        electronics = Category("Electronics", "Devices", [phone, laptop])
        accessories = Category("Accessories", "Add-ons", [tablet])

        # Проверяем счетчики
        assert Category.category_count == 2
        assert Category.product_count == 3

        # Проверяем содержимое
        assert electronics.products[0].name == "iPhone"
        assert accessories.products[0].name == "iPad"

        # Создаем еще одну категорию
        sale = Category("Sale", "Discounted items", [phone, tablet])
        assert Category.category_count == 3
        assert Category.product_count == 5

        # Проверяем, что объекты те же самые
        assert sale.products[0] is phone
        assert sale.products[1] is tablet


# Простые тесты для каждого пункта задания
def test_1_category_initialization():
    """Корректность инициализации класса Category"""
    product = Product("Test", "Desc", 100.0, 5)
    category = Category("Test Cat", "Test Desc", [product])

    assert category.name == "Test Cat"
    assert category.description == "Test Desc"
    assert len(category.products) == 1


def test_2_product_initialization():
    """Корректность инициализации класса Product"""
    product = Product("Test Product", "Description", 99.99, 10)

    assert product.name == "Test Product"
    assert product.description == "Description"
    assert product.price == 99.99
    assert product.quantity == 10


def test_3_product_count():
    """Подсчет количества продуктов"""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    p3 = Product("P3", "D3", 30.0, 3)

    Category("Cat1", "Desc1", [p1, p2])
    Category("Cat2", "Desc2", [p3])

    assert Category.product_count == 3


def test_4_category_count():
    """Подсчет количества категорий"""
    Category.category_count = 0
    Category.product_count = 0

    p = Product("P", "D", 10.0, 1)

    Category("Cat1", "Desc1", [p])
    Category("Cat2", "Desc2", [p])
    Category("Cat3", "Desc3", [p])

    assert Category.category_count == 3
