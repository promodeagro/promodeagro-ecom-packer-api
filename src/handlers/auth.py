# Auth Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
import random
import time
from src.commonfunctions.utils import format_response

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_dotenv()

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ.get('USERS_TABLE', 'prod-promodeagro-packerTable-Users')

def login(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        password = body.get('password')
        if not email or not password:
            logger.warning('Missing email or password')
            return format_response(400, {'message': 'Email and password are required.'})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user or user.get('password') != password:
            logger.info(f"User from DB: {user}")
            logger.info(f"Password from request: '{password}'")
            logger.info(f"Password from DB: '{user.get('password') if user else None}'")
            logger.info(f'Invalid login attempt for email: {email}')
            return format_response(401, {'message': 'Invalid credentials'})
        # IGNORE TOKEN: Token logic is disabled for development/testing
        # token = 'dummy-token-for-' + email
        # return format_response(200, {'token': token, 'user_id': user.get('user_id', email)})
        return format_response(200, {'user_id': user.get('user_id', email)})
    except Exception as e:
        logger.error(f'Login error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def forgot_password(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        if not email:
            logger.warning('Missing email for forgot password')
            return format_response(400, {'message': 'Email is required.'})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user:
            logger.info(f'Forgot password: Email not found: {email}')
            return format_response(404, {'message': 'Email not found'})
        # Generate a new random 6-digit OTP every time
        otp = str(random.randint(100000, 999999))
        otp_expiry = int(time.time()) + 300  # 5 minutes from now
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET otp = :otp, otp_expiry = :otp_expiry',
            ExpressionAttributeValues={':otp': otp, ':otp_expiry': otp_expiry}
        )
        logger.info(f'OTP for {email} is {otp} (expires at {otp_expiry})')  # Show OTP and expiry in console
        return format_response(200, {'message': 'OTP sent successfully'})
    except Exception as e:
        logger.error(f'Forgot password error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def verify_otp(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        otp = body.get('otp')
        if not email or not otp:
            logger.warning('Missing email or otp for verify')
            return format_response(400, {'message': 'Email and OTP are required.'})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user or user.get('otp') != otp:
            logger.info(f'Invalid OTP for {email}')
            return format_response(401, {'message': 'Invalid OTP'})
        # Check OTP expiry
        otp_expiry = user.get('otp_expiry')
        now = int(time.time())
        if not otp_expiry or now > int(otp_expiry):
            logger.info(f'OTP expired for {email}')
            return format_response(401, {'message': 'OTP expired'})
        # Optionally clear OTP after verification
        table.update_item(
            Key={'email': email},
            UpdateExpression='REMOVE otp, otp_expiry'
        )
        logger.info(f'OTP verified for {email}')
        return format_response(200, {'message': 'OTP verified'})
    except Exception as e:
        logger.error(f'OTP verify error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def reset_password(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        new_password = body.get('new_password')
        confirm_password = body.get('confirm_password')
        if not email or not new_password or not confirm_password:
            logger.warning('Missing fields for reset password')
            return format_response(400, {'message': 'Email, new password, and confirm password are required.'})
        if new_password != confirm_password:
            logger.info(f'Passwords do not match for {email}')
            return format_response(400, {'message': "Passwords don't match"})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user:
            logger.info(f'Reset password: Email not found: {email}')
            return format_response(404, {'message': 'Email not found'})
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET password = :pw',
            ExpressionAttributeValues={':pw': new_password}
        )
        logger.info(f'Password reset for {email}')
        return format_response(200, {'message': 'Password reset successful'})
    except Exception as e:
        logger.error(f'Reset password error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def logout(event, context):
    try:
        # Invalidate token logic would go here (if using JWT, add to blacklist, etc.)
        logger.info('User logged out')
        return format_response(200, {'message': 'Logged out successfully'})
    except Exception as e:
        logger.error(f'Logout error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)}) 