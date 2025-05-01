import os
import sys
from typing import Dict, Any

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import validate_user_token

# Lambda handler
def handler(event: Dict[str, Any], context: Any) -> Dict[str, bool]:
    return validate_user_token.validate_user_token(event, context)