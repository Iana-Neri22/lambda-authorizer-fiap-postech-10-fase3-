import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Log the incoming event
        logger.info('Received event: %s', json.dumps(event))
        
        # Validate the event structure
        if 'authorizationToken' not in event:
            logger.error('Missing authorizationToken in event')
            raise ValueError('Missing authorizationToken in event')
            
        auth = 'Deny'
        
        # Validate the token
        if event['authorizationToken'] == 'abc123':
            auth = 'Allow'
            logger.info('Token validation successful')
        else:
            logger.warning('Invalid token provided')
            auth = 'Deny'
        
        # Construct the response
        auth_response = {
            "principalId": "abc123",
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