import json
import logging
import random
import string
import hashlib
import os
import decimal

def format_response(status_code, body):
    """Format a standard API Gateway response with CORS headers."""
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        }
    }

def generate_otp(length=6):
    """Generate a numeric OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))

def hash_password(password):
    """Hash a password using SHA-256 (for demonstration; use bcrypt/argon2 in production)."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash."""
    return hash_password(password) == hashed

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def require_auth(event):
    # IGNORE AUTH: Authorization check is disabled for development/testing
    # headers = event.get('headers', {})
    # headers_lower = {k.lower(): v for k, v in headers.items()}
    # logger.info(f"Headers received: {headers_lower}")  # For debugging
    # auth_header = headers_lower.get('authorization')
    # if not auth_header:
    #     return ({
    #         'statusCode': 401,
    #         'body': json.dumps({'message': 'Authorization token is missing.'})
    #     }, None)
    # if not auth_header.lower().startswith('bearer '):
    #     return ({
    #         'statusCode': 401,
    #         'body': json.dumps({'message': 'Authorization token format is invalid.'})
    #     }, None)
    # token = auth_header.split(' ', 1)[1]
    # return (None, token)
    return (None, "dummy-token")

def get_logger(name=__name__):
    """Get a configured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        # Convert to int if possible, else float
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj 