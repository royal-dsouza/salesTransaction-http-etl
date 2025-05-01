"""
Main Cloud Run service module for the Sales ETL microservice.
Handles HTTP requests, orchestrates validation, transformation, and loading to BigQuery.
"""
import logging
from flask import request, jsonify
import functions_framework
from pydantic import ValidationError

from schema import validate_transaction
from transform import transform_record
from bigquery_loader import insert_into_bigquery
from config import BIGQUERY_TABLE_ID, SERVICE_ACCOUNT_FILE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.http
def process_sales_transaction(request):
    """
    Cloud Function entry point: Process sales transaction data from HTTP request.
    Validates, transforms, and loads data to BigQuery.
    
    Args:
        request (flask.Request): HTTP request object
        
    Returns:
        flask.Response: JSON response with processing status
    """
    if request.method != 'POST':
        return jsonify({'error': 'Only POST requests are supported'}), 405

    try:
        transaction_data = request.get_json()
        if not transaction_data:
            return jsonify({'error': 'No JSON data provided'}), 400
    except Exception as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        return jsonify({'error': 'Invalid JSON format'}), 400

    try:
        # Step 1: Validate input using Pydantic
        is_valid, result = validate_transaction(transaction_data)

        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': 'Schema validation failed',
                'errors': result
            }), 400

        transaction_dict = result.dict()

        # Step 2: Transform data (add tax, timestamp, total)
        transformed_data = transform_record(transaction_dict)

        # Step 3: Load to BigQuery
        insert_into_bigquery(transformed_data, BIGQUERY_TABLE_ID)

        return jsonify({
            'status': 'success',
            'message': 'Transaction processed successfully',
            'transaction_id': transformed_data.get('transaction_id'),
            'processed_at': transformed_data.get('processed_at')  # correct key
        }), 201

    except ValidationError as e:
        logger.warning(f"Schema validation failed: {e.errors()}")
        return jsonify({
            'status': 'error',
            'message': 'Schema validation failed',
            'errors': e.errors()
        }), 400

    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': f'Error processing transaction: {str(e)}'
        }), 500
