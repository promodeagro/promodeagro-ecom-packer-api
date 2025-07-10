# Notifications Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
from src.commonfunctions.utils import require_auth, format_response, convert_decimal

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
NOTIFICATION_TABLE = os.environ.get('NOTIFICATION_TABLE', 'prod-promodeagro-packerTable-notification')

def get_notifications(event, context):
    # IGNORE TOKEN: Token logic is disabled for development/testing
    try:
        user_id = event.get('queryStringParameters', {}).get('user_id')
        if not user_id:
            logger.warning('Missing user_id for notifications')
            return format_response(400, {'message': 'user_id is required'})
        table = dynamodb.Table(NOTIFICATION_TABLE)
        response = table.query(
            IndexName='user_id-index',
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        notifications = response.get('Items', [])
        notifications = convert_decimal(notifications)
        logger.info(f'Retrieved {len(notifications)} notifications for user {user_id}')
        return format_response(200, notifications)
    except Exception as e:
        logger.error(f'Get notifications error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)}) 