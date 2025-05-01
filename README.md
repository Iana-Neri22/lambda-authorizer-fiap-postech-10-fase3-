# Lambda Authorizer with JWT and CPF

This is a Lambda authorizer that uses JWT tokens for authentication based on CPF (Brazilian individual taxpayer registration).

## Setup

1. Create a new Lambda function in AWS
2. Upload the `lambda_function.py` file
3. Install the required dependencies (PyJWT) in a ZIP file and upload it
4. Set the following environment variable in your Lambda configuration:
   - `JWT_SECRET`: Your secret key for JWT token signing

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