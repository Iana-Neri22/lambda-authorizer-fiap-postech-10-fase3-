import json
import logging
import secrets
import string

from src.gateway.cliente_gateway import get_cliente_by_cpf

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_token(cpf):
    cliente = get_cliente_by_cpf(cpf)
    if cliente:
        """Generate a secure random token"""
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(32))
        return token
    else:
        return None

def validate_token(token):
    """Validate the provided token"""
    # In a real implementation, you would validate against a database or other storage
    # For this example, we'll just check if it's a valid format
    return len(token) == 32 and all(c in string.ascii_letters + string.digits for c in token)

def generate_token_handler(event, context):
    try:
        logger.info('Generating new token')
        token = generate_token()
        
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "token": token
            })
        }
        
        logger.info('Token generated successfully')
        return response
        
    except Exception as e:
        logger.error('Error generating token: %s', str(e))
        raise

def lambda_handler(event, context):
    try:
        # Log the incoming event
        logger.info('Received event: %s', json.dumps(event))
        
        # Validate the event structure
        if 'authorizationToken' not in event:
            logger.error('Missing authorizationToken in event')
            raise ValueError('Missing authorizationToken in event')

        authorization_token = event['authorizationToken']
        auth = 'Deny'
        
        # Validate the token
        if validate_token(authorization_token):
            auth = 'Allow'
            logger.info('Token validation successful')
        else:
            logger.warning('Invalid token provided')
            auth = 'Deny'
        
        # Construct the response
        auth_response = {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Resource": ["arn:aws:execute-api:us-east-1:692859918281:8u45isczl8/*/*"],
                        "Effect": auth
                    }
                ]
            }
        }
        
        logger.info('Returning auth response: %s', json.dumps(auth_response))
        return auth_response
        
    except Exception as e:
        logger.error('Error processing request: %s', str(e))
        raise