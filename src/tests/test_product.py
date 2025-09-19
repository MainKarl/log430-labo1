import pytest
from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()

def test_product_select():
    product_list = dao.select_all()
    assert len(product_list) >= 3

def test_product_insert():
    product = Product(None, 'Car4', 'Test_brand', 100.0)
    dao.insert(product)
    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name in names

def test_product_update():
    product = Product(None, 'Car5', 'Ferrari', 250.0)
    assigned_id = dao.insert(product)

    corrected_name = 'Car5_v2'
    product.id = assigned_id
    product.name = corrected_name
    product.brand = 'Ferrari'
    product.price = 300.0

    dao.update(product)

    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert corrected_name in names

def test_product_delete():
    product = Product(None, 'Car6', 'Ferrari', 100.0)
    assigned_id = dao.insert(product)
    dao.delete(assigned_id)

    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name not in names