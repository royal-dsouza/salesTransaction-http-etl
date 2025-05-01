import logging
from google.cloud import bigquery
from google.oauth2 import service_account
from config import SERVICE_ACCOUNT_FILE

# Set up logging configuration
logger = logging.getLogger(__name__)

# Load credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

def insert_into_bigquery(row, table_id):
    """
    Inserts a single row of data into a BigQuery table.

    Args:
        row (dict): A JSON-serializable dictionary representing the row to insert.
        table_id (str): The full BigQuery table ID in the format 'project.dataset.table'.

    Returns:
        dict: A success message if the insert succeeds.

    Raises:
        RuntimeError: If one or more insert errors occur.
    """
    # Create BigQuery client with credentials
    client = bigquery.Client(credentials=credentials)

    logger.info("Attempting to insert row into BigQuery: %s", row)

    # Insert the row using the BigQuery client
    errors = client.insert_rows_json(table_id, [row])

    if errors:
        # Log each error individually and raise a RuntimeError
        for error in errors:
            error_message = f"BigQuery insert error for Transaction: {row.get('transaction_id')} - {error}"
            logger.error(error_message)
        raise RuntimeError(
            f"BigQuery insert for Transaction {row.get('transaction_id')} failed with {len(errors)} error(s)."
        )
    else:
        logger.info("Transaction: %s successfully loaded into BigQuery", row.get("transaction_id"))
