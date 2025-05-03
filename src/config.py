"""
Configuration parameters for the Sales ETL microservice.
"""

import os

# BigQuery settings (from environment variables with default fallback)
PROJECT_ID = os.getenv("GCP_PROJECT", "elevated-column-458305-f8")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "Sales_Transaction_HTTP")
TABLE_NAME = os.getenv("BIGQUERY_TABLE", "transaction")

# Fully qualified BigQuery table ID
BIGQUERY_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

# Optional: Path to service account key file (local dev only)
# SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/Users/royaldsouza/Downloads/my_gcp_project.json") # for local development
