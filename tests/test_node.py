import pytest
from ldfparser.node import LinProductId

@pytest.mark.unit()
def test_lin_product_id_create_valid():
    LinProductId.create(supplier_id=0x0001, function_id=0x0002, variant=1)

@pytest.mark.unit()
def test_lin_product_id_create_invalid_supplier():
    with pytest.raises(ValueError):
        LinProductId.create(supplier_id=0xFFFF, function_id=0x0002, variant=1)

@pytest.mark.unit()
def test_lin_product_id_create_invalid_function():
    with pytest.raises(ValueError):
        LinProductId.create(supplier_id=0x0001, function_id=0xFFFFFFFF, variant=1)

@pytest.mark.unit()
def test_lin_product_id_create_invalid_variant():
    with pytest.raises(ValueError):
        LinProductId.create(supplier_id=0x0001, function_id=0x0002, variant=-1)
