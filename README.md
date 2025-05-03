# Lambda Authorizer with JWT and CPF

This is a Lambda authorizer that uses JWT tokens for authentication based on CPF (Brazilian individual taxpayer registration).

## Prerequisites

1. Node.js and npm installed
2. Python 3.11 or later installed
3. AWS account and credentials configured
4. Serverless Framework account

## Setup

1. Configure your AWS credentials:
   ```bash
   aws configure
   ```

2. Install the Serverless Framework globally:
   ```bash
   npm install -g serverless
   ```

3. Login to your Serverless Framework account:
   ```bash
   serverless login
   ```

4. Install project dependencies:
   ```bash
   make install
   ```

## Makefile Commands

The project includes a Makefile with the following commands:

- `make install`: Installs all Python dependencies from requirements.txt
- `make deploy`: Deploys the Lambda function to AWS using Serverless Framework
- `make test`: Runs the test suite
- `make clean`: Removes build artifacts and cache files

## API Endpoint

After deployment, your Lambda function will be available at:
```
https://3mpv0zx0jl.execute-api.us-east-1.amazonaws.com/dev/authorize
```

## How it Works

The authorizer expects a JWT token in the Authorization header of the request. The token should contain a CPF field.

### Token Generation

To generate a token, you can use the `generate_token` function:

```python
token = generate_token("123.456.789-00")
```

### API Gateway Configuration

1. In API Gateway, create a new authorizer
2. Select "Lambda" as the authorizer type
3. Select your Lambda function
4. Set the "Token Source" to "Authorization" header

### Making Authenticated Requests

Include the JWT token in your requests using the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Security Considerations

1. Always use HTTPS in production
2. Store the JWT_SECRET in AWS Secrets Manager or Parameter Store
3. Consider implementing rate limiting
4. Regularly rotate your JWT_SECRET

## Error Handling

The authorizer will return:
- Allow: If the token is valid and contains a CPF
- Deny: If the token is missing, invalid, expired, or doesn't contain a CPF 

-- API Gateway Endpoint
https://3mpv0zx0jl.execute-api.us-east-1.amazonaws.com/dev/cliente

-- Deploy through the CLI
serverless deploy