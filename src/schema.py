import logging
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, Tuple, Any, Dict, Union

# --------------------------
# Set up basic logging
# --------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------
# Pydantic model for validating incoming sales transaction data
# --------------------------
class SaleTransaction(BaseModel):
    """
    Represents a single sales transaction.

    Fields:
    - transaction_id: Required unique transaction identifier.
    - product_id: Required product identifier.
    - amount: Required float representing the sale amount.
    - currency: Required currency code (e.g., "USD").
    - customer_id: Optional customer ID.
    """
    transaction_id: str
    product_id: str
    amount: float = Field(gt=0)
    customer_id: Optional[str] = None

# --------------------------
# Validate input data against the SaleTransaction schema
# --------------------------
def validate_transaction(data: Dict[str, Any]) -> Tuple[bool, Union[SaleTransaction, list]]:
    """
    Validates a dictionary of data against the SaleTransaction model.

    Args:
        data (dict): The incoming JSON-like payload to validate.

    Returns:
        Tuple[bool, Union[SaleTransaction, list]]:
            - (True, SaleTransaction) if validation succeeds.
            - (False, list of validation errors) if validation fails.
    """
    try:
        validated = SaleTransaction(**data)
        logger.info("Validation succeeded for transaction_id: %s", data.get("transaction_id"))
        return True, validated
    except ValidationError as e:
        logger.warning("Validation failed for input: %s", data)
        logger.error("Validation errors: %s", e.errors())
        return False, e.errors()
