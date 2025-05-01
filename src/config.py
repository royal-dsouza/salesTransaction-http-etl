
"""
Configuration parameters for the Sales ETL microservice.
"""

# BigQuery settings
PROJECT_ID = "elevated-column-458305-f8"
DATASET_ID = "Sales_Transaction_HTTP"
TABLE_NAME = "transaction"

# Fully qualified BigQuery table ID
BIGQUERY_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

SERVICE_ACCOUNT_FILE = "/Users/royaldsouza/Downloads/my_gcp_project.json"