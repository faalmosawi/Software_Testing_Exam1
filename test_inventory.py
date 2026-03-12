"""
Exam 1 - Test Inventory Module
================================
Write your tests below. Each section (Part A through E) is marked.
Follow the instructions in each part carefully.

Run your tests with:
    pytest test_inventory.py -v

Run with coverage:
    pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
"""

import pytest
from unittest.mock import patch
from inventory import (
    add_product,
    get_product,
    update_stock,
    calculate_total,
    apply_bulk_discount,
    list_products,
)
import inventory


# ============================================================
# FIXTURE: Temporary inventory file (provided for you)
# This ensures each test gets a clean, isolated inventory.
# ============================================================

@pytest.fixture(autouse=True)
def clean_inventory(tmp_path, monkeypatch):
    """Use a temporary inventory file for each test."""
    db_file = str(tmp_path / "inventory.json")
    monkeypatch.setattr("inventory.INVENTORY_FILE", db_file)
    yield


# ============================================================
# PART A - Basic Assertions (18 marks)
# Write at least 8 tests using plain assert statements.
# Cover: add_product, get_product, update_stock,
#        calculate_total, and list_products.
# Follow the AAA pattern (Arrange, Act, Assert).
# ============================================================

# TODO: Write your Part A tests here

#1. Test Add Products
def test_add_product():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 3

    # Act 
    result = add_product(product_id, name, price, stock)

    #Assert 
    assert result == {"product_id": product_id, "name": name, "price": price, "stock": stock}

#2. Test Get Product
def test_get_product():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 3

    # Act 
    add_product(product_id, name, price, stock)
    result = get_product(product_id)

    #Assert 
    assert result == {"product_id": '1', "name": name, "price": price, "stock": stock}

#3. Test Get Product with non existing product_id
def test_get_product_with_non_existing_product_id():
    # Arrange
    product_id = '1'

    # Act 
    result = get_product(product_id)

    #Assert 
    assert result == None

#4. Test Update Stock
def test_update_stock():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 20

    # Act 
    add_product(product_id, name, price, stock)
    update_stock(product_id, 5) # increase stock by 5
    result = get_product(product_id)

    #Assert 
    assert result == {"product_id": '1', "name": name, "price": price, "stock": 25}
    
    update_stock(product_id, -10) # decrease stock by 10
    result = get_product(product_id)    
    assert result == {"product_id": '1', "name": name, "price": price, "stock": 15}

#5. Test Calculate Total
def test_calculate_total():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 9.99
    stock = 3
    quantity = 3

    # Act 
    add_product(product_id, name, price, stock)
    result = calculate_total(product_id, quantity)

    #Assert 
    assert result == 29.97 


#6. Test List Products
def test_list_products():
    # Arrange
    product_id1 = '1'
    name1 = "Test Product 1"
    price1 = 5
    stock1 = 3

    product_id2 = '2'
    name2 = "Test Product 2"
    price2 = 10
    stock2 = 5

    # Act 
    add_product(product_id1, name1, price1, stock1)
    add_product(product_id2, name2, price2, stock2)
    result = list_products()

    #Assert 
    assert len(result) == 2
    assert {"product_id": '1', "name": name1, "price": price1, "stock": stock1} in result
    assert {"product_id": '2', "name": name2, "price": price2, "stock": stock2} in result

#7. Test Apply Bulk Discount
def test_apply_bulk_discount_for_10_items():
    # Arrange
    quantity = 10
    total = 100

    # Act
    result = apply_bulk_discount(total, quantity)

    # Assert
    assert result == round(total * (1 - 0.05), 2)

#8. Test Apply Bulk Discount for 50 items
def test_apply_bulk_discount_for_50_items():
    # Arrange
    quantity = 50
    total = 100

    # Act
    result = apply_bulk_discount(total, quantity)

    # Assert
    assert result == round(total * (1 - 0.15), 2)


# ============================================================
# PART B - Exception Testing (12 marks)
# Write at least 6 tests using pytest.raises.
# Cover: empty name, negative price, duplicate product,
#        stock going below zero, product not found, etc.
# ============================================================

# TODO: Write your Part B tests here
#9. Test Add Product with empty product id
def test_add_product_with_empty_product_id():
    # Arrange
    name = "Test Product 1"
    price = 5
    stock = 3

    #Act
    with pytest.raises(ValueError) as err:
        add_product(product_id='', name=name,price=price, stock=stock)
    
    # #Assert
    # assert str(err.value) == "Product ID and name are required"

#10. Test Add Product with empty name
def test_add_product_with_empty_name():
    # Arrange
    product_id = '1'
    price = 5
    stock = 3

    #Act
    with pytest.raises(ValueError) as err:
        add_product(product_id=product_id, name="",price=price, stock=stock)
    
    # #Assert
    # assert str(err.value) == "Product ID and name are required"

#11. Test Add Product with negative price
def test_add_product_with_negative_price():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = -5
    stock = 3

    #Act
    with pytest.raises(ValueError) as err:
        add_product(product_id, name, price, stock)
    
    # #Assert
    # assert str(err.value) == "Price must be positive"

#12. Test Add Product with negative stock
def test_add_product_with_negative_stock():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = -3

    #Act
    with pytest.raises(ValueError) as err:
        add_product(product_id, name, price, stock)
    
    # #Assert
    # assert str(err.value) == "Stock cannot be negative"

#13. Test Add Product with duplicate product_id
def test_add_product_with_duplicate_product_id():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 3

    # Act 
    add_product(product_id, name, price, stock) # Add first time
    with pytest.raises(ValueError) as err:
        add_product(product_id, name, price, stock)
    
    # # Assert
    # assert str(err.value) == f"Product '{product_id}' already exists"

#14. Test Update Stock with negative stock
def test_update_stock_with_negative_stock():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 3

    # Act
    add_product(product_id, name, price, stock)
    with pytest.raises(ValueError) as err:
        update_stock(product_id, -4) # decrease stock by 4
    
    # # Assert
    # assert str(err.value) == "Stock cannot go below zero"

#15. Test Update Stock with non existing product_id
def test_update_stock_with_non_existing_product_id():
    # Arrange
    product_id = '1'

    # Act
    with pytest.raises(ValueError) as err:
        update_stock(product_id, 3) 
    
    # # Assert
    # assert str(err.value) == f"Product '{product_id}' not found"

#16. Test Calculate Total with negative quantity
def test_calculate_total_with_negative_quantity():
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 3
    quantity = -2

    add_product(product_id, name, price, stock)
    with pytest.raises(ValueError) as err:
        calculate_total(product_id, quantity)

# ============================================================
# PART C - Fixtures and Parametrize (10 marks)
#
# C1: Create a @pytest.fixture called "sample_products" that
#     adds 3 products to the inventory and returns their IDs.
#     Write 2 tests that use this fixture.
#
# C2: Use @pytest.mark.parametrize to test apply_bulk_discount
#     with at least 5 different (total, quantity, expected) combos.
# ============================================================

# TODO: Write your Part C tests here
@pytest.fixture
def sample_products():
    add_product("P001", "Laptop", 999.99, 10)
    add_product("P002", "Mouse", 29.99, 50)
    add_product("P003", "Keyboard", 79.99, 25)
    
    return ["P001", "P002", "P003"]

#17. Test list products by using the fixure
def test_list_products_with_sample_products(sample_products):
    products = list_products()
    assert len(products) == 3
    assert any(pr["product_id"] == "P001" for pr in products)
    assert any(pr["product_id"] == "P002" for pr in products)
    assert any(pr["product_id"] == "P003" for pr in products)

#18. Test calculate total by using the fixure
def test_calculate_total_with_sample_products(sample_products):
    total = calculate_total("P001", 2) 
    assert total == 1999.98

@pytest.mark.parametrize("total, quantity, expected", [
    (100, 9, 100.00),  # no discount
    (100, 3, 100.00),  # no discount
    (100, 20, 95.00),   # 5% discount
    (100, 30, 90.00),  # 10% discount
    (100, 60, 85.00),  # 15% discount
])
#19. Test apply_bulk_discount using parametrize
def test_apply_bulk_discount_parametrized(total, quantity, expected):
    result = apply_bulk_discount(total, quantity)
    assert result == expected


# ============================================================
# PART D - Mocking (5 marks)
# Use @patch to mock _send_restock_alert.
# Write 2 tests:
#   1. Verify the alert IS called when stock drops below 5
#   2. Verify the alert is NOT called when stock stays >= 5
# ============================================================


# TODO: Write your Part D tests here

@patch("inventory._send_restock_alert")
def test_restock_alert_called(mock_alert):
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 6

    # Act
    add_product(product_id, name, price, stock)
    update_stock(product_id, -3)

    # Assert
    mock_alert.assert_called_once_with(product_id, name, 3)

@patch("inventory._send_restock_alert")
def test_restock_alert_not_called(mock_alert):
    # Arrange
    product_id = '1'
    name = "Test Product 1"
    price = 5
    stock = 20

    # Act
    add_product(product_id, name, price, stock)
    update_stock(product_id, -5)

    # Assert
    mock_alert.assert_not_called()

# ============================================================
# PART E - Coverage (5 marks)
# Run: pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
# You must achieve 90%+ coverage on inventory.py.
# If lines are missed, add more tests above to cover them.
# ============================================================


# ============================================================
# BONUS (5 extra marks)
# 1. Add a function get_low_stock_products(threshold) to
#    inventory.py that returns all products with stock < threshold.
# 2. Write 3 parametrized tests for it below.
# ============================================================

# TODO: Write your bonus tests here (optional)