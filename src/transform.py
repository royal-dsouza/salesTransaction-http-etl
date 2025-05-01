import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms a sales transaction record by:
    - Calculating 10% tax on the amount.
    - Adding a processing timestamp.
    - Calculating the total amount (amount + tax).

    Args:
        record (dict): A validated transaction record.

    Returns:
        dict: The enriched transaction record with 'tax', 'processed_at', and 'total_amount' fields added.
    """
    logger.info("Starting transformation for record: %s", record)

    try:
        # round the amount to 2 decimal
        record['amount'] = round(record['amount'],2)
        
        # Calculate 10% tax and round to 2 decimal places
        record['tax'] = round(record['amount'] * 0.1, 2)

        # Add current timestamp in ISO format
        record['processed_at'] = datetime.now().isoformat()

        # Compute total amount
        record['total_amount'] = round(record['amount'] + record['tax'], 2)

        logger.info("Successfully transformed record: %s", record)
        return record

    except Exception as e:
        logger.error("Error transforming record: %s", e, exc_info=True)
        raise
