# Auth Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

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
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Email and password are required.'})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user or user.get('password') != password:
            logger.info(f'Invalid login attempt for email: {email}')
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid credentials'})
            }
        # Simulate token generation (replace with real JWT in production)
        token = 'dummy-token-for-' + email
        logger.info(f'User {email} logged in successfully')
        return {
            'statusCode': 200,
            'body': json.dumps({'token': token, 'user_id': user.get('user_id', email)})
        }
    except Exception as e:
        logger.error(f'Login error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def forgot_password(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        if not email:
            logger.warning('Missing email for forgot password')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Email is required.'})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user:
            logger.info(f'Forgot password: Email not found: {email}')
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Email not found'})
            }
        # Simulate OTP generation and store (in production, send via email/SMS)
        otp = '123456'  # Replace with real OTP logic
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET otp = :otp',
            ExpressionAttributeValues={':otp': otp}
        )
        logger.info(f'OTP sent to {email}')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'OTP sent successfully'})
        }
    except Exception as e:
        logger.error(f'Forgot password error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def verify_otp(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        otp = body.get('otp')
        if not email or not otp:
            logger.warning('Missing email or otp for verify')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Email and OTP are required.'})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user or user.get('otp') != otp:
            logger.info(f'Invalid OTP for {email}')
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid OTP'})
            }
        # Optionally clear OTP after verification
        table.update_item(
            Key={'email': email},
            UpdateExpression='REMOVE otp'
        )
        logger.info(f'OTP verified for {email}')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'OTP verified'})
        }
    except Exception as e:
        logger.error(f'OTP verify error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def reset_password(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        new_password = body.get('new_password')
        confirm_password = body.get('confirm_password')
        if not email or not new_password or not confirm_password:
            logger.warning('Missing fields for reset password')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Email, new password, and confirm password are required.'})
            }
        if new_password != confirm_password:
            logger.info(f'Passwords do not match for {email}')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "Passwords don't match"})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user:
            logger.info(f'Reset password: Email not found: {email}')
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Email not found'})
            }
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET password = :pw',
            ExpressionAttributeValues={':pw': new_password}
        )
        logger.info(f'Password reset for {email}')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Password reset successful'})
        }
    except Exception as e:
        logger.error(f'Reset password error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def logout(event, context):
    try:
        # Invalidate token logic would go here (if using JWT, add to blacklist, etc.)
        logger.info('User logged out')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Logged out successfully'})
        }
    except Exception as e:
        logger.error(f'Logout error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        } 