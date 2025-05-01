import json
import os
import jwt
from typing import Any, Dict, Optional
from gateway.cliente_gateway import get_cliente_by_cpf

def validate_user_token(event: Dict[str, Any], context: Any) -> Dict[str, bool]:
    """
    Lambda function to validate user token and check if user exists in database.
    
    Args:
        event: Lambda event containing the authorization header
        context: Lambda context object
        
    Returns:
        Dict containing isAuthorized boolean
    """
    auth_header = event.get('headers', {}).get('authorization', '')
    auth_parts = auth_header.split(' ')
    
    if len(auth_parts) != 2 or auth_parts[0] != 'Bearer':
        return {'isAuthorized': False}
    
    token = auth_parts[1]
    
    try:
        # Verify the JWT token
        verified_token = jwt.decode(
            token,
            os.environ['PUBLIC_KEY'],
            algorithms=['RS256']
        )
        
        cpf = verified_token.get('cpf')
        if cpf:
            # Check if user exists in database
            results = get_cliente_by_cpf(cpf)
            if not results or len(results) == 0:
                return {'isAuthorized': False}
        
        return {'isAuthorized': True}
        
    except Exception as e:
        print(f"Error validating token: {str(e)}")
        return {'isAuthorized': False}

