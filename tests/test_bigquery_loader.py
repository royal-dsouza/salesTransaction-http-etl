# tests/test_bigquery_loader.py
import pytest
from src.bigquery_loader import insert_into_bigquery

def test_successful_insert(mocker):
    # Mock the BigQuery client and its insert_rows_json method
    mock_client_class = mocker.patch("src.bigquery_loader.bigquery.Client")
    mock_client = mock_client_class.return_value
    mock_client.insert_rows_json.return_value = []

    test_row = {
        "transaction_id": "TX100",
        "product_id": "P100",
        "amount": 100.0,
        "customer_id": "CUST100",
        "tax": 10.0,
        "processed_at": "2025-04-30T10:00:00",
        "total_amount": 110.0
    }

    insert_into_bigquery(test_row, "project.dataset.table")

    # Assert insert was called once with expected arguments
    mock_client.insert_rows_json.assert_called_once_with("project.dataset.table", [test_row])

def test_failed_insert_raises_error(mocker):
    mock_client_class = mocker.patch("src.bigquery_loader.bigquery.Client")
    mock_client = mock_client_class.return_value
    mock_client.insert_rows_json.return_value = [{"index": 0, "errors": ["Invalid row"]}]

    test_row = {
        "transaction_id": "TX101",
        "product_id": "P101",
        "amount": 100.0,
        "customer_id": "CUST101",
        "tax": 10.0,
        "processed_at": "2025-04-30T10:00:00",
        "total_amount": 110.0
    }

    with pytest.raises(RuntimeError, match="BigQuery insert"):
        insert_into_bigquery(test_row, "project.dataset.table")
