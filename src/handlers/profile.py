from dotenv import load_dotenv
load_dotenv()

# Profile Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from src.commonfunctions.utils import require_auth, format_response, convert_decimal
import decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ.get('USERS_TABLE', 'prod-promodeagro-packerTable-Users')

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

def get_profile(event, context):
    # IGNORE AUTH: Authorization check is disabled for development/testing
    # error, token = require_auth(event)
    # if error:
    #     return error
    try:
        email = event.get('queryStringParameters', {}).get('email')
        if not email:
            logger.warning('Missing email for get_profile')
            return format_response(400, {'message': 'email is required'})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user:
            logger.info(f'User not found: {email}')
            return format_response(404, {'message': 'User not found'})
        user = convert_decimal(user)
        logger.info(f'Retrieved profile for {email}')
        return format_response(200, user)
    except Exception as e:
        logger.error(f'Get profile error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def update_profile(event, context):
    # IGNORE AUTH: Authorization check is disabled for development/testing
    # error, token = require_auth(event)
    # if error:
    #     return error
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        username = body.get('username')
        if not email or not username:
            logger.warning('Missing fields for update_profile')
            return format_response(400, {'message': 'email and username are required'})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user:
            logger.info(f'User not found: {email}')
            return format_response(404, {'message': 'User not found'})
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET username = :u',
            ExpressionAttributeValues={':u': username}
        )
        logger.info(f'Profile updated for {email}')
        return format_response(200, {'message': 'Profile updated'})
    except Exception as e:
        logger.error(f'Update profile error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def change_password(event, context):
    # IGNORE AUTH: Authorization check is disabled for development/testing
    # error, token = require_auth(event)
    # if error:
    #     return error
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        current_password = body.get('current_password')
        new_password = body.get('new_password')
        confirm_password = body.get('confirm_password')
        if not email or not current_password or not new_password or not confirm_password:
            logger.warning('Missing fields for change_password')
            return format_response(400, {'message': 'All fields are required (email, current_password, new_password, confirm_password)'})
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'email': email})
        user = response.get('Item')
        if not user or user.get('password') != current_password:
            logger.info(f'Current password incorrect for {email}')
            return format_response(400, {'message': 'Current password is incorrect'})
        if new_password != confirm_password:
            logger.info(f'Passwords do not match for {email}')
            return format_response(400, {'message': "Passwords don't match"})
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET password = :pw',
            ExpressionAttributeValues={':pw': new_password}
        )
        logger.info(f'Password changed for {email}')
        return format_response(200, {'message': 'Password changed'})
    except Exception as e:
        logger.error(f'Change password error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)}) 