import os
import json
import tempfile

from main import Product, Category, load_categories_from_json


class TestProduct:
    """Тесты для класса Product"""

    def test_product_initialization_correctness(self):
        """Тест 1: корректность инициализации объектов класса Product"""
        product = Product("iPhone 15", "512GB, Black Titanium", 129990.0, 10)

        assert product.name == "iPhone 15", "Название продукта не совпадает"
        assert product.description == "512GB, Black Titanium", "Описание продукта не совпадает"
        assert product.price == 129990.0, "Цена продукта не совпадает"
        assert product.quantity == 10, "Количество продукта не совпадает"

    def test_product_initialization_with_different_data_types(self):
        """Проверка разных типов данных для продукта"""
        # Целочисленная цена
        product_int = Product("Test Phone", "Description", 100, 5)
        assert isinstance(product_int.price, float), "Цена должна быть float"
        assert product_int.price == 100.0

        # Дробная цена
        product_float = Product("Test Phone 2", "Description", 99.99, 3)
        assert product_float.price == 99.99

        # Нулевое количество
        product_zero = Product("Out of Stock", "No stock", 1000.0, 0)
        assert product_zero.quantity == 0


class TestCategory:
    """Тесты для класса Category"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization_correctness(self):
        """Тест корректности инициализации объектов класса Category"""
        product1 = Product(
            "Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5
        )
        product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

        category = Category("Смартфоны", "Мобильные телефоны", [product1, product2])

        assert category.name == "Смартфоны", "Название категории не совпадает"
        assert category.description == "Мобильные телефоны", "Описание категории не совпадает"
        assert len(category.products) == 2, "Количество продуктов в категории не совпадает"
        assert category.products[0] is product1, "Первый продукт не совпадает"
        assert category.products[1] is product2, "Второй продукт не совпадает"

    def test_category_initialization_with_empty_products(self):
        """Тест инициализации категории с пустым списком продуктов"""
        category = Category("Пустая категория", "Без продуктов", [])

        assert category.name == "Пустая категория"
        assert len(category.products) == 0

    def test_category_product_count_calculation(self):
        """Тест подсчета количества продуктов"""
        product1 = Product("Product A", "Description A", 100.0, 5)
        product2 = Product("Product B", "Description B", 200.0, 3)
        product3 = Product("Product C", "Description C", 300.0, 7)

        # Создаем первую категорию с 2 продуктами
        category1 = Category("Category 1", "First category", [product1, product2])
        assert Category.product_count == 2, "После первой категории должно быть 2 продукта"

        # Создаем вторую категорию с 1 продуктом
        category2 = Category("Category 2", "Second category", [product3])
        assert Category.product_count == 3, "После второй категории должно быть 3 продукта"

        # Создаем третью категорию с 2 продуктами (один из них повторяется)
        category3 = Category("Category 3", "Third category", [product1, product3])
        assert Category.product_count == 5, "После третьей категории должно быть 5 продуктов"

    def test_category_count_calculation(self):
        """Тест 4: подсчет количества категорий"""
        product = Product("Test Product", "Description", 100.0, 5)

        category1 = Category("Category 1", "First", [product])
        assert Category.category_count == 1, "Должна быть 1 категория"

        category2 = Category("Category 2", "Second", [product])
        assert Category.category_count == 2, "Должно быть 2 категории"

        category3 = Category("Category 3", "Third", [product])
        assert Category.category_count == 3, "Должно быть 3 категории"

    def test_category_count_with_multiple_categories(self):
        """Дополнительный тест: подсчет категорий в разных сценариях"""
        product = Product("Test", "Desc", 100.0, 1)

        categories = []
        for i in range(5):
            cat = Category(f"Category {i}", f"Description {i}", [product])
            categories.append(cat)

        assert Category.category_count == 5, "Должно быть 5 категорий"
        assert len(categories) == 5

    def test_product_count_with_duplicate_products(self):
        """Дополнительный тест: подсчет продуктов с учетом дубликатов"""
        product1 = Product("Phone", "Smartphone", 500.0, 10)
        product2 = Product("Phone", "Smartphone", 500.0, 10)  # Технически другой объект

        Category("Cat1", "Desc1", [product1])
        Category("Cat2", "Desc2", [product2])

        assert Category.product_count == 2, "Должно быть 2 продукта"


class TestCategoryProductCounters:
    """Тесты для проверки счетчиков категорий и продуктов"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_counters_reset_properly(self):
        """Проверка корректного сброса счетчиков"""
        assert Category.category_count == 0, "Счетчик категорий должен быть 0"
        assert Category.product_count == 0, "Счетчик продуктов должен быть 0"

    def test_counters_increment_with_multiple_objects(self):
        """Проверка увеличения счетчиков при создании объектов"""
        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)
        product3 = Product("P3", "D3", 30.0, 3)

        Category("Cat1", "Desc1", [product1])  # 1 категория, 1 продукт
        Category("Cat2", "Desc2", [product1, product2])  # 2 категория, +2 продукта
        Category("Cat3", "Desc3", [product1, product2, product3])  # 3 категория, +3 продукта

        assert Category.category_count == 3, "Должно быть 3 категории"
        assert Category.product_count == 6, "Должно быть 6 продуктов (1+2+3)"


class TestLoadCategoriesFromJSON:
    """Тесты для функции загрузки из JSON"""

    def setup_method(self):
        """Подготовка временного JSON файла"""
        self.sample_json_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices",
                "products": [
                    {
                        "name": "Laptop",
                        "description": "Gaming laptop",
                        "price": 150000.0,
                        "quantity": 10
                    },
                    {
                        "name": "Mouse",
                        "description": "Wireless mouse",
                        "price": 2500.0,
                        "quantity": 50
                    }
                ]
            },
            {
                "name": "Books",
                "description": "Fiction books",
                "products": [
                    {
                        "name": "Python Programming",
                        "description": "Learn Python",
                        "price": 3500.0,
                        "quantity": 100
                    }
                ]
            }
        ]

    def test_load_categories_from_json(self):
        """Тест загрузки категорий из JSON файла"""
        # Создаем временный JSON файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(self.sample_json_data, f, ensure_ascii=False)
            temp_file_path = f.name

        try:
            categories = load_categories_from_json(temp_file_path)

            assert len(categories) == 2, "Должно быть 2 категории"

            # Проверяем первую категорию
            assert categories[0].name == "Electronics"
            assert categories[0].description == "Electronic devices"
            assert len(categories[0].products) == 2
            assert categories[0].products[0].name == "Laptop"
            assert categories[0].products[0].price == 150000.0

            # Проверяем вторую категорию
            assert categories[1].name == "Books"
            assert len(categories[1].products) == 1
            assert categories[1].products[0].name == "Python Programming"

        finally:
            # Удаляем временный файл
            os.unlink(temp_file_path)

    def test_load_categories_from_empty_json(self):
        """Тест загрузки из пустого JSON"""
        empty_data = []

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(empty_data, f)
            temp_file_path = f.name

        try:
            categories = load_categories_from_json(temp_file_path)
            assert len(categories) == 0, "Должен быть пустой список"
        finally:
            os.unlink(temp_file_path)


# Функциональные тесты (без классов)
def test_product_initialization_basic():
    """Простой тест инициализации продукта (пункт 2 задания)"""
    product = Product("Test", "Desc", 100.0, 5)
    assert product.name == "Test"
    assert product.quantity == 5


def test_category_initialization_basic():
    """Тест инициализации категории"""
    product = Product("Test", "Desc", 100.0, 5)
    category = Category("Test Cat", "Test Desc", [product])
    assert category.name == "Test Cat"
    assert len(category.products) == 1


def test_product_count_basic():
    """Тест подсчета продуктов"""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)

    Category("Cat1", "Desc1", [p1, p2])
    assert Category.product_count == 2


def test_category_count_basic():
    """Тест подсчета категорий"""
    Category.category_count = 0
    Category.product_count = 0

    p = Product("P", "D", 10.0, 1)

    Category("Cat1", "Desc1", [p])
    Category("Cat2", "Desc2", [p])

    assert Category.category_count == 2
