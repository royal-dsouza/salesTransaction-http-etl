
# tests/test_transform.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from transform import transform_record
from datetime import datetime

def test_standard_transformation():
    record = {
        "transaction_id": "TX001",
        "product_id": "P001",
        "amount": 200.0,
        "customer_id": "CUST001"
    }
    result = transform_record(record)
    assert result["tax"] == 20.0
    assert result["total_amount"] == 220.0
    assert "processed_at" in result
    # Ensure it is a string
    assert isinstance(result["processed_at"], str)
    # Try parsing it to verify it's a valid ISO format datetime
    parsed = datetime.fromisoformat(result["processed_at"])
    assert isinstance(parsed, datetime)

def test_high_precision_amount():
    record = {
        "transaction_id": "TX003",
        "product_id": "P001",
        "amount": 123.4567,
        "customer_id": "CUST003"
    }
    result = transform_record(record)
    assert result['amount'] == 123.46
    assert result["tax"] == 12.35
    assert result["total_amount"] == 135.81
