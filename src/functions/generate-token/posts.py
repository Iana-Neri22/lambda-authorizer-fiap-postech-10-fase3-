import json
import jwt
from typing import Dict, Any
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
import os
from gateway.cliente_gateway import get_cliente_by_cpf

def api_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }

def is_valid_cpf(cpf: str) -> bool:
    return len(cpf) == 11

def handler(event: APIGatewayProxyEvent, context: LambdaContext) -> Dict[str, Any]:
    try:
        body = json.loads(event.body or '{}')
        cpf = body.get('cpf')

        if not cpf or not is_valid_cpf(cpf):
            return api_response(400, {'error': 'Invalid CPF'})

        if not get_cliente_by_cpf(cpf):
            return api_response(404, {'error': 'User not found'})

        token = jwt.encode(
            {'cpf': cpf},
            os.environ['PRIVATE_KEY'],
            algorithm='RS256',
            expires_in=os.environ['TOKEN_EXPIRATION_TIME']
        )

        return api_response(200, {'token': token})

    except Exception as error:
        print(f"Error: {str(error)}")
        return api_response(500, {'error': 'Internal Server Error'})
