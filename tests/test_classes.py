import os
import pytest
import json
import tempfile

from src.class_product import Product, Smartphone, LawnGrass
from src.class_category import Category
from src.from_jason import load_categories_from_json


class TestProduct:
    """Полные тесты для класса Product"""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Category.category_count = 0
        Category.product_count = 0


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

    def test_product_str_method_with_zero_quantity(self):
        """Тест продукта с нулевым количеством"""
        product = Product("Out of Stock", "Description", 50.0, 0)
        expected = "Out of Stock, 50 руб. Остаток: 0 шт."
        assert str(product) == expected

    def test_product_with_large_numbers(self):
        """Тест продукта с большими числами"""
        product = Product("Expensive Item", "Luxury", 1_000_000.0, 9999)
        assert product.price == 1_000_000.0
        assert product.quantity == 9999

    def test_product_with_string_price_conversion(self):
        """Тест: цена должна быть числом"""
        product = Product("Test", "Desc", 100, 5)
        assert isinstance(product.price, (int, float))

    def test_product_attributes_are_mutable(self, monkeypatch):
        """Тест: атрибуты продукта можно изменять"""
        product = Product("Phone", "Smartphone", 500.0, 10)

        product.name = "New Phone"

        # Мокируем input для подтверждения понижения цены
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        product.price = 450.0
        product.quantity = 8

        assert product.name == "New Phone"
        assert product.price == 450.0
        assert product.quantity == 8

    # Тесты для нового функционала - __str__

    def test_product_str_method(self):
        """Тест строкового представления продукта"""
        product = Product("Test Product", "Description", 99.99, 15)
        expected = "Test Product, 99.99 руб. Остаток: 15 шт."
        assert str(product) == expected

    def test_product_str_method_with_zero_quantity(self):
        """Тест строкового представления продукта с нулевым количеством"""
        product = Product("Out of Stock", "Description", 50.0, 0)
        expected = "Out of Stock, 50 руб. Остаток: 0 шт."
        assert str(product) == expected

    def test_product_str_method_with_integer_price(self):
        """Тест строкового представления продукта с целочисленной ценой"""
        product = Product("Cheap Item", "Description", 100, 5)
        expected = "Cheap Item, 100 руб. Остаток: 5 шт."
        assert str(product) == expected

    # Тесты для нового функционала - __add__

    def test_product_add_method(self):
        """Тест сложения двух продуктов"""
        product_a = Product("Product A", "Desc", 100.0, 10)
        product_b = Product("Product B", "Desc", 200.0, 2)

        result = product_a + product_b
        expected = 100 * 10 + 200 * 2  # 1000 + 400 = 1400
        assert result == expected

    def test_product_add_method_with_large_numbers(self):
        """Тест сложения продуктов с большими числами"""
        product_a = Product("Expensive A", "Desc", 1000.0, 100)
        product_b = Product("Expensive B", "Desc", 2000.0, 50)

        result = product_a + product_b
        expected = 1000 * 100 + 2000 * 50  # 100000 + 100000 = 200000
        assert result == expected

    def test_product_add_method_with_zero_quantity(self):
        """Тест сложения продуктов, где один имеет нулевое количество"""
        product_a = Product("Product A", "Desc", 100.0, 10)
        product_b = Product("Product B", "Desc", 200.0, 0)

        result = product_a + product_b
        expected = 100 * 10 + 200 * 0  # 1000 + 0 = 1000
        assert result == expected

    def test_product_add_method_with_zero_price(self):
        """Тест сложения продуктов, где один имеет нулевую цену"""
        product_a = Product("Product A", "Desc", 100.0, 10)
        product_b = Product("Free Product", "Desc", 0.0, 5)

        result = product_a + product_b
        expected = 100 * 10 + 0 * 5  # 1000 + 0 = 1000
        assert result == expected

    def test_product_add_method_with_same_product(self):
        """Тест сложения продукта с самим собой"""
        product = Product("Product", "Desc", 100.0, 10)
        result = product + product
        expected = 100 * 10 + 100 * 10  # 1000 + 1000 = 2000
        assert result == expected

    def test_product_add_method_invalid_type(self):
        """Тест сложения продукта с объектом другого типа"""
        product = Product("Product", "Desc", 100.0, 10)

        def add_with_int():
            return product + 100  # type: ignore

        with pytest.raises(TypeError, match="Невозможно сложить Product с int"):
            add_with_int()

    # Остальные существующие тесты...

    def test_add_product_to_category(self):
        """Тест добавления продукта в категорию через add_product"""
        product1 = Product("Product A", "Desc A", 100.0, 5)
        category = Category("Electronics", "Devices", [product1])

        product2 = Product("Product B", "Desc B", 200.0, 3)
        category.add_product(product2)

        products_list = category.get_products_list()
        assert len(products_list) == 2
        assert products_list[1] is product2

    def test_add_product_increments_product_count(self):
        """Тест увеличения счетчика продуктов при добавлении"""
        product1 = Product("P1", "D1", 100.0, 5)
        category = Category("Cat1", "Desc1", [product1])

        assert Category.product_count == 1

        product2 = Product("P2", "D2", 200.0, 3)
        category.add_product(product2)

        assert Category.product_count == 2

    def test_add_multiple_products_to_category(self):
        """Тест добавления нескольких продуктов в категорию"""
        category = Category("Empty", "No products", [])

        for i in range(5):
            product = Product(f"P{i}", f"D{i}", 100.0, i)
            category.add_product(product)

        products_list = category.get_products_list()
        assert len(products_list) == 5
        assert Category.product_count == 5

    def test_category_products_getter_format(self):
        """Тест геттера products - проверка формата вывода"""
        product1 = Product("Phone", "Smartphone", 500.0, 10)
        product2 = Product("Laptop", "Computer", 1500.0, 5)

        category = Category("Electronics", "Devices", [product1, product2])

        products_str = category.products
        assert "Phone, 500 руб. Остаток: 10 шт." in products_str
        assert "Laptop, 1500 руб. Остаток: 5 шт." in products_str
        
    def test_category_products_getter_empty(self):
        """Тест геттера products для пустой категории"""
        category = Category("Empty", "No products", [])
        assert category.products == "В категории нет товаров"

    def test_category_products_getter_after_add_product(self):
        """Тест геттера products после добавления продукта"""
        product1 = Product("Phone", "Smartphone", 500.0, 10)
        category = Category("Electronics", "Devices", [product1])

        assert "Phone, 500 руб. Остаток: 10 шт." in category.products

        product2 = Product("Tablet", "iPad", 800.0, 8)
        category.add_product(product2)

        assert "Tablet, 800 руб. Остаток: 8 шт." in category.products

    # Тесты для нового функционала категории - __str__

    def test_category_str_method(self):
        """Тест строкового представления категории"""
        product1 = Product("P1", "D1", 100.0, 5)
        product2 = Product("P2", "D2", 200.0, 3)
        product3 = Product("P3", "D3", 300.0, 7)

        category = Category("Electronics", "Devices", [product1, product2, product3])
        expected = "Electronics, количество продуктов: 15 шт."  # 5 + 3 + 7 = 15
        assert str(category) == expected

    def test_category_str_method_empty_category(self):
        """Тест строкового представления пустой категории"""
        category = Category("Empty", "No products", [])
        expected = "Empty, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_str_method_single_product(self):
        """Тест строкового представления категории с одним продуктом"""
        product = Product("Single", "Desc", 100.0, 10)
        category = Category("Single Cat", "Desc", [product])
        expected = "Single Cat, количество продуктов: 10 шт."
        assert str(category) == expected

    def test_category_str_method_with_zero_quantity_products(self):
        """Тест строкового представления категории с продуктами нулевого количества"""
        product1 = Product("P1", "D1", 100.0, 0)
        product2 = Product("P2", "D2", 200.0, 5)
        category = Category("Mixed", "Desc", [product1, product2])
        expected = "Mixed, количество продуктов: 5 шт."  # 0 + 5 = 5
        assert str(category) == expected

    # Тесты для итератора (дополнительное задание)

    def test_category_iterator(self):
        """Тест итератора категории"""
        product1 = Product("P1", "D1", 100.0, 5)
        product2 = Product("P2", "D2", 200.0, 3)
        product3 = Product("P3", "D3", 300.0, 7)

        category = Category("Test Cat", "Desc", [product1, product2, product3])

        products_from_iteration = []
        for product in category:
            products_from_iteration.append(product)

        assert len(products_from_iteration) == 3
        assert products_from_iteration[0] is product1
        assert products_from_iteration[1] is product2
        assert products_from_iteration[2] is product3

    def test_category_iterator_empty_category(self):
        """Тест итератора для пустой категории"""
        category = Category("Empty", "No products", [])

        products_from_iteration = []
        for product in category:
            products_from_iteration.append(product)

        assert len(products_from_iteration) == 0

    def test_category_iterator_manual(self):
        """Тест ручного использования итератора"""
        product1 = Product("P1", "D1", 100.0, 5)
        product2 = Product("P2", "D2", 200.0, 3)

        category = Category("Test Cat", "Desc", [product1, product2])

        iterator = iter(category)
        assert next(iterator) is product1
        assert next(iterator) is product2
        with pytest.raises(StopIteration):
            next(iterator)

    # Остальные существующие тесты для Product...

    def test_new_product_without_existing_products(self):
        """Тест new_product без проверки существующих продуктов"""
        product_data = {
            "name": "New Phone",
            "description": "Latest model",
            "price": 999.99,
            "quantity": 20
        }

        product = Product.new_product(product_data)

        assert product.name == "New Phone"
        assert product.description == "Latest model"
        assert product.price == 999.99
        assert product.quantity == 20

    def test_new_product_with_duplicate_same_price(self):
        """Тест new_product с дубликатом и одинаковой ценой"""
        existing_product = Product("iPhone", "Smartphone", 1000.0, 5)
        existing_products = [existing_product]

        product_data = {
            "name": "iPhone",
            "description": "Smartphone",
            "price": 1000.0,
            "quantity": 3
        }

        result = Product.new_product(product_data, existing_products)

        assert result is existing_product
        assert result.quantity == 8  # 5 + 3
        assert result.price == 1000.0  # Цена осталась прежней

    def test_new_product_with_duplicate_higher_price(self):
        """Тест new_product с дубликатом и более высокой ценой"""
        existing_product = Product("iPhone", "Smartphone", 1000.0, 5)
        existing_products = [existing_product]

        product_data = {
            "name": "iPhone",
            "description": "Smartphone",
            "price": 1200.0,
            "quantity": 3
        }

        result = Product.new_product(product_data, existing_products)

        assert result is existing_product
        assert result.quantity == 8  # 5 + 3
        assert result.price == 1200.0  # Выбрана максимальная цена

    def test_new_product_with_duplicate_lower_price(self):
        """Тест new_product с дубликатом и более низкой ценой"""
        existing_product = Product("iPhone", "Smartphone", 1000.0, 5)
        existing_products = [existing_product]

        product_data = {
            "name": "iPhone",
            "description": "Smartphone",
            "price": 800.0,
            "quantity": 3
        }

        result = Product.new_product(product_data, existing_products)

        assert result is existing_product
        assert result.quantity == 8  # 5 + 3
        assert result.price == 1000.0  # Оставлена более высокая цена

    def test_new_product_with_multiple_existing_products(self):
        """Тест new_product с несколькими существующими продуктами"""
        existing_products = [
            Product("iPhone", "Smartphone", 1000.0, 5),
            Product("Samsung", "Android", 900.0, 10),
            Product("Pixel", "Google", 800.0, 3)
        ]

        product_data = {
            "name": "Samsung",
            "description": "Android",
            "price": 950.0,
            "quantity": 7
        }

        result = Product.new_product(product_data, existing_products)

        assert result.name == "Samsung"
        assert result.quantity == 17  # 10 + 7
        assert result.price == 950.0

    def test_product_price_getter(self):
        """Тест геттера цены"""
        product = Product("Test", "Desc", 100.0, 5)
        assert product.price == 100.0

    def test_product_price_setter_invalid_negative(self, capsys):
        """Тест сеттера цены с отрицательным значением"""
        product = Product("Test", "Desc", 100.0, 5)

        product.price = -50
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

    def test_product_price_setter_invalid_zero(self, capsys):
        """Тест сеттера цены с нулевым значением"""
        product = Product("Test", "Desc", 100.0, 5)

        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

    def test_product_price_setter_valid_increase(self):
        """Тест сеттера цены с увеличением цены"""
        product = Product("Test", "Desc", 100.0, 5)
        product.price = 150.0
        assert product.price == 150.0

    def test_product_price_setter_valid_decrease_with_confirmation(self, monkeypatch):
        """Тест сеттера цены с понижением цены и подтверждением (y)"""
        product = Product("Test", "Desc", 100.0, 5)

        monkeypatch.setattr('builtins.input', lambda _: 'y')

        product.price = 80.0
        assert product.price == 80.0

    def test_product_price_setter_valid_decrease_with_cancellation(self, monkeypatch):
        """Тест сеттера цены с понижением цены и отменой (n)"""
        product = Product("Test", "Desc", 100.0, 5)

        monkeypatch.setattr('builtins.input', lambda _: 'n')

        product.price = 80.0
        assert product.price == 100.0  # Цена не изменилась


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

    def test_category_with_empty_products(self):
        """Тест категории без продуктов"""
        category = Category("Empty", "No products", [])

        assert category.name == "Empty"
        assert Category.product_count == 0

    def test_category_with_single_product(self):
        """Тест категории с одним продуктом"""
        product = Product("Single", "Only one", 100.0, 1)
        category = Category("Single Category", "Just one product", [product])

        assert Category.product_count == 1

    def test_category_counters_with_multiple_categories(self):
        """Тест счетчиков при создании нескольких категорий"""
        p1 = Product("P1", "D1", 10.0, 1)
        p2 = Product("P2", "D2", 20.0, 2)
        p3 = Product("P3", "D3", 30.0, 3)

        Category("Cat1", "Desc1", [p1])
        assert Category.category_count == 1
        assert Category.product_count == 1

        Category("Cat2", "Desc2", [p1, p2])
        assert Category.category_count == 2
        assert Category.product_count == 3

        Category("Cat3", "Desc3", [p1, p2, p3])
        assert Category.category_count == 3
        assert Category.product_count == 6

    def test_products_private_attribute(self):
        """Тест: атрибут products должен быть приватным"""
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test", "Desc", [product])

        # Проверяем, что атрибут недоступен напрямую
        with pytest.raises(AttributeError):
            _ = category.__products  # type: ignore

        # Дополнительная проверка
        assert hasattr(category, '_Category__products')

    def test_get_products_list_returns_correct_list(self):
        """Тест метода get_products_list"""
        product1 = Product("P1", "D1", 100.0, 5)
        product2 = Product("P2", "D2", 200.0, 3)

        category = Category("Cat", "Desc", [product1, product2])

        products_list = category.get_products_list()
        assert isinstance(products_list, list)
        assert len(products_list) == 2
        assert products_list[0] is product1
        assert products_list[1] is product2


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

            products_list = categories[0].get_products_list()
            assert len(products_list) == 2
            assert products_list[0].name == "Phone"
            assert products_list[1].name == "Laptop"
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
            assert len(categories[0].get_products_list()) == 0
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
        phone = Product("iPhone", "Smartphone", 1000.0, 10)
        laptop = Product("MacBook", "Laptop", 2000.0, 5)
        tablet = Product("iPad", "Tablet", 500.0, 8)

        electronics = Category("Electronics", "Devices", [phone, laptop])
        accessories = Category("Accessories", "Add-ons", [tablet])

        assert Category.category_count == 2
        assert Category.product_count == 3

        assert "iPhone, 1000 руб. Остаток: 10 шт." in electronics.products  # Убрали .0

        electronics.add_product(tablet)
        assert Category.product_count == 4

        existing_products = [phone, laptop, tablet]
        new_phone_data = {
            "name": "iPhone",
            "description": "Smartphone",
            "price": 1100.0,
            "quantity": 5
        }

        updated_phone = Product.new_product(new_phone_data, existing_products)
        assert updated_phone is phone
        assert phone.quantity == 15
        assert phone.price == 1100.0

    def test_new_product_with_add_product_integration(self):
        """Интеграционный тест: new_product и add_product вместе"""
        existing_product = Product("Laptop", "Gaming", 1500.0, 3)
        category = Category("Computers", "Devices", [existing_product])

        product_data = {
            "name": "Laptop",
            "description": "Gaming",
            "price": 1600.0,
            "quantity": 2
        }

        result = Product.new_product(product_data, category.get_products_list())

        assert result.quantity == 5
        assert result.price == 1600.0

        category_products = category.get_products_list()
        assert category_products[0] is result


def test_category_initialization():
    """Корректность инициализации класса Category"""
    product = Product("Test", "Desc", 100.0, 5)
    category = Category("Test Cat", "Test Desc", [product])

    assert category.name == "Test Cat"
    assert category.description == "Test Desc"
    assert len(category.get_products_list()) == 1


def test_product_initialization():
    """Корректность инициализации класса Product"""
    product = Product("Test Product", "Description", 99.99, 10)

    assert product.name == "Test Product"
    assert product.description == "Description"
    assert product.price == 99.99
    assert product.quantity == 10


def test_product_count():
    """Подсчет количества продуктов"""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    p3 = Product("P3", "D3", 30.0, 3)

    Category("Cat1", "Desc1", [p1, p2])
    Category("Cat2", "Desc2", [p3])

    assert Category.product_count == 3


def test_category_count():
    """Подсчет количества категорий"""
    Category.category_count = 0
    Category.product_count = 0

    p = Product("P", "D", 10.0, 1)

    Category("Cat1", "Desc1", [p])
    Category("Cat2", "Desc2", [p])
    Category("Cat3", "Desc3", [p])

    assert Category.category_count == 3


def test_add_product_method():
    """Тест метода add_product."""
    Category.category_count = 0
    Category.product_count = 0

    product = Product("Test", "Desc", 100.0, 5)
    category = Category("Cat", "Desc", [])

    category.add_product(product)
    products_list = category.get_products_list()

    assert len(products_list) == 1
    assert products_list[0] is product
    assert Category.product_count == 1


def test_products_getter_format():
    """Тест геттера products"""
    product = Product("Phone", "Smartphone", 500.0, 10)
    category = Category("Electronics", "Devices", [product])

    result = category.products
    assert result == "Phone, 500 руб. Остаток: 10 шт."


def test_products_getter_empty():
    """Тест геттера products для пустой категории."""
    category = Category("Empty", "No products", [])
    assert category.products == "В категории нет товаров"


def test_new_product_classmethod():
    """Тест класс-метода new_product."""
    product_data = {
        "name": "New Device",
        "description": "Latest tech",
        "price": 999.99,
        "quantity": 15
    }

    product = Product.new_product(product_data)

    assert product.name == "New Device"
    assert product.price == 999.99
    assert product.quantity == 15


def test_new_product_with_duplicate():
    """Тест new_product с проверкой дубликатов."""
    existing = Product("iPhone", "Phone", 1000.0, 5)

    product_data = {
        "name": "iPhone",
        "description": "Phone",
        "price": 1200.0,
        "quantity": 3
    }

    result = Product.new_product(product_data, [existing])

    assert result is existing
    assert result.quantity == 8
    assert result.price == 1200.0


def test_price_setter_invalid():
    """Тест сеттера цены с некорректными значениями."""
    product = Product("Test", "Desc", 100.0, 5)

    product.price = -50
    assert product.price == 100.0

    product.price = 0
    assert product.price == 100.0


def test_price_setter_valid():
    """Тест сеттера цены с корректными значениями."""
    product = Product("Test", "Desc", 100.0, 5)

    product.price = 150.0
    assert product.price == 150.0


# 16.1. Тесты для классов-наследников

class TestSmartphone:
    """Тесты для класса Smartphone"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_smartphone_initialization(self):
        """Тест корректной инициализации смартфона"""
        smartphone = Smartphone(
            "Xiaomi 13 Pro", "Флагман", 89990.0, 15,
            "высокая", "13 Pro", 512, "черный"
        )

        assert smartphone.name == "Xiaomi 13 Pro"
        assert smartphone.description == "Флагман"
        assert smartphone.price == 89990.0
        assert smartphone.quantity == 15
        assert smartphone.efficiency == "высокая"
        assert smartphone.model == "13 Pro"
        assert smartphone.memory == 512
        assert smartphone.color == "черный"

    def test_smartphone_inherits_from_product(self):
        """Тест: Smartphone является наследником Product"""
        smartphone = Smartphone("Test", "Desc", 100.0, 5, "high", "M1", 128, "red")
        assert isinstance(smartphone, Product)
        assert issubclass(Smartphone, Product)

    def test_smartphone_str_method(self):
        """Тест строкового представления смартфона"""
        smartphone = Smartphone("iPhone 15", "Flagship", 99990.0, 10, "high", "15 Pro", 256, "black")
        expected = "iPhone 15, 99990.0 руб. Остаток: 10 шт."
        assert str(smartphone) == expected

    def test_smartphone_add_same_type(self):
        """Тест сложения двух смартфонов"""
        s1 = Smartphone("S1", "D1", 100.0, 10, "high", "M1", 128, "red")
        s2 = Smartphone("S2", "D2", 200.0, 5, "high", "M2", 256, "blue")
        result = s1 + s2
        expected = 100 * 10 + 200 * 5  # 1000 + 1000 = 2000
        assert result == expected


class TestLawnGrass:
    """Тесты для класса LawnGrass"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_lawn_grass_initialization(self):
        """Тест корректной инициализации газонной травы"""
        grass = LawnGrass(
            "Газон 'Изумруд'", "Спортивный газон", 1500.0, 50,
            "Россия", 14, "зеленый"
        )

        assert grass.name == "Газон 'Изумруд'"
        assert grass.description == "Спортивный газон"
        assert grass.price == 1500.0
        assert grass.quantity == 50
        assert grass.country == "Россия"
        assert grass.germination_period == 14
        assert grass.color == "зеленый"

    def test_lawn_grass_inherits_from_product(self):
        """Тест: LawnGrass является наследником Product"""
        grass = LawnGrass("Test", "Desc", 100.0, 5, "Russia", 10, "green")
        assert isinstance(grass, Product)
        assert issubclass(LawnGrass, Product)

    def test_lawn_grass_str_method(self):
        """Тест строкового представления газонной травы"""
        grass = LawnGrass("Green Lawn", "Beautiful", 2000.0, 20, "Germany", 14, "green")
        expected = "Green Lawn, 2000.0 руб. Остаток: 20 шт."
        assert str(grass) == expected

    def test_lawn_grass_add_same_type(self):
        """Тест сложения двух газонных трав"""
        g1 = LawnGrass("G1", "D1", 100.0, 10, "Russia", 14, "green")
        g2 = LawnGrass("G2", "D2", 150.0, 4, "Germany", 21, "dark green")
        result = g1 + g2
        expected = 100 * 10 + 150 * 4  # 1000 + 600 = 1600
        assert result == expected


class TestProductAddRestriction:
    """Тесты для ограничения сложения (Задание 2)"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_with_smartphone_works(self):
        """Тест: сложение двух смартфонов работает"""
        s1 = Smartphone("S1", "D1", 100.0, 10, "high", "M1", 128, "red")
        s2 = Smartphone("S2", "D2", 200.0, 5, "high", "M2", 256, "blue")
        result = s1 + s2
        assert result == 2000.0

    def test_add_product_with_lawn_grass_works(self):
        """Тест: сложение двух трав работает"""
        g1 = LawnGrass("G1", "D1", 100.0, 10, "Russia", 14, "green")
        g2 = LawnGrass("G2", "D2", 150.0, 4, "Germany", 21, "dark green")
        result = g1 + g2
        assert result == 1600.0

    def test_add_product_different_classes_raises_error(self):
        """Тест: сложение товаров разных классов вызывает TypeError"""
        smartphone = Smartphone("S1", "D1", 100.0, 10, "high", "M1", 128, "red")
        grass = LawnGrass("G1", "D1", 100.0, 10, "Russia", 14, "green")
        product = Product("P1", "D1", 100.0, 10)

        with pytest.raises(TypeError, match="Невозможно сложить товары разных классов"):
            _ = smartphone + grass

        with pytest.raises(TypeError, match="Невозможно сложить товары разных классов"):
            _ = smartphone + product

        with pytest.raises(TypeError, match="Невозможно сложить товары разных классов"):
            _ = grass + product

    def test_add_same_class_instances_works(self):
        """Тест: сложение экземпляров одного класса работает"""
        p1 = Product("P1", "D1", 100.0, 5)
        p2 = Product("P2", "D2", 200.0, 3)
        result = p1 + p2
        assert result == 100 * 5 + 200 * 3


class TestCategoryAddProductRestriction:
    """Тесты для ограничения добавления продуктов (Задание 3)"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_valid_types(self):
        """Тест: добавление допустимых типов продуктов"""
        category = Category("Test", "Desc", [])
        product = Product("P1", "D1", 100.0, 5)
        smartphone = Smartphone("S1", "D1", 100.0, 5, "high", "M1", 128, "red")
        grass = LawnGrass("G1", "D1", 100.0, 5, "Russia", 14, "green")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category.get_products_list()) == 3

    def test_add_product_invalid_type_raises_error(self):
        """Тест: добавление объекта неправильного типа вызывает TypeError"""
        category = Category("Test", "Desc", [])

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product("not a product")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(123)

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product(None)

        assert len(category.get_products_list()) == 0

    def test_add_product_none_instance(self):
        """Тест: добавление None вызывает ошибку"""
        category = Category("Test", "Desc", [])

        with pytest.raises(TypeError):
            category.add_product(None)

    def test_add_product_with_duplicate_name_allowed(self):
        """Тест: добавление продукта с существующим именем разрешено"""
        category = Category("Test", "Desc", [])
        product1 = Product("Phone", "D1", 100.0, 5)
        product2 = Product("Phone", "D2", 150.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        # Оба продукта добавлены, так как это разные объекты
        assert len(category.get_products_list()) == 2


class TestInheritanceIntegration:
    """Интеграционные тесты для классов-наследников"""

    def setup_method(self):
        Category.category_count = 0
        Category.product_count = 0

    def test_mixed_category_contains_different_types(self):
        """Тест: категория может содержать разные типы продуктов"""
        category = Category("Store", "All products", [])

        product = Product("Simple", "Desc", 100.0, 5)
        smartphone = Smartphone("Phone", "Desc", 500.0, 3, "high", "X1", 128, "black")
        grass = LawnGrass("Grass", "Desc", 50.0, 100, "Russia", 14, "green")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        assert len(category.get_products_list()) == 3
        assert Category.product_count == 3

    def test_category_str_with_mixed_products(self):
        """Тест: строковое представление категории со смешанными продуктами"""
        category = Category("Mixed", "All types", [])

        product = Product("P1", "D1", 100.0, 5)
        smartphone = Smartphone("S1", "D1", 200.0, 3, "high", "M1", 128, "red")
        grass = LawnGrass("G1", "D1", 50.0, 10, "Russia", 14, "green")

        category.add_product(product)
        category.add_product(smartphone)
        category.add_product(grass)

        expected = "Mixed, количество продуктов: 18 шт."  # 5 + 3 + 10 = 18
        assert str(category) == expected
