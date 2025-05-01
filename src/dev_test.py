"""
Local development server for testing Cloud Functions locally.
This avoids the forking issues when using functions-framework directly.
"""
import os
import logging
from flask import Flask, request
from main import process_sales_transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def local_function():
    """Wrapper around the Cloud Function for local testing"""
    return process_sales_transaction(request)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)