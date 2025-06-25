import json
import logging
import random
import string
import hashlib

def format_response(status_code, body):
    """Format a standard API Gateway response."""
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
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