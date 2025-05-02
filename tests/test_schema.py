# tests/test_schema.py
import pytest
from src.schema import validate_transaction

@pytest.mark.parametrize("transaction,expected", [
    (   # Valid input
        {
            "transaction_id": "TX001",
            "product_id": "P001",
            "amount": 100.0,
            "customer_id": "CUST001"
        },
        True
    ),
    (   # Missing transaction_id
        {
            "product_id": "P001",
            "amount": 100.0,
            "customer_id": "CUST001"
        },
        False
    ),
    (   # Negative amount
        {
            "transaction_id": "TX003",
            "product_id": "P001",
            "amount": -50.0,
            "customer_id": "CUST001"
        },
        False
    ),
    (   # Missing product_id
        {
            "transaction_id": "TX004",
            "amount": 120.0,
            "customer_id": "CUST001"
        },
        False
    ),
])
def test_transaction_schema(transaction, expected):
    is_valid, result = validate_transaction(transaction)
    assert is_valid == expected
