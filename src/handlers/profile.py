from dotenv import load_dotenv
load_dotenv()

# Profile Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ.get('USERS_TABLE', 'prod-promodeagro-packerTable-Users')

def get_profile(event, context):
    try:
        user_id = event.get('queryStringParameters', {}).get('user_id')
        if not user_id:
            logger.warning('Missing user_id for get_profile')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'user_id is required'})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'user_id': user_id})
        user = response.get('Item')
        if not user:
            logger.info(f'User not found: {user_id}')
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
        logger.info(f'Retrieved profile for {user_id}')
        return {
            'statusCode': 200,
            'body': json.dumps(user)
        }
    except Exception as e:
        logger.error(f'Get profile error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def update_profile(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('user_id')
        username = body.get('username')
        email = body.get('email')
        if not user_id or not username or not email:
            logger.warning('Missing fields for update_profile')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'user_id, username, and email are required'})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'user_id': user_id})
        user = response.get('Item')
        if not user:
            logger.info(f'User not found: {user_id}')
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET username = :u, email = :e',
            ExpressionAttributeValues={':u': username, ':e': email}
        )
        logger.info(f'Profile updated for {user_id}')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Profile updated'})
        }
    except Exception as e:
        logger.error(f'Update profile error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def change_password(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('user_id')
        current_password = body.get('current_password')
        new_password = body.get('new_password')
        confirm_password = body.get('confirm_password')
        if not user_id or not current_password or not new_password or not confirm_password:
            logger.warning('Missing fields for change_password')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'All fields are required'})
            }
        if new_password != confirm_password:
            logger.info(f'Passwords do not match for {user_id}')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "Passwords don't match"})
            }
        table = dynamodb.Table(USERS_TABLE)
        response = table.get_item(Key={'user_id': user_id})
        user = response.get('Item')
        if not user or user.get('password') != current_password:
            logger.info(f'Current password incorrect for {user_id}')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Current password is incorrect'})
            }
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET password = :pw',
            ExpressionAttributeValues={':pw': new_password}
        )
        logger.info(f'Password changed for {user_id}')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Password changed'})
        }
    except Exception as e:
        logger.error(f'Change password error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        } 