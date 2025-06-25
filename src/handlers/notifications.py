# Notifications Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
NOTIFICATION_TABLE = os.environ.get('NOTIFICATION_TABLE', 'prod-promodeagro-packerTable-notification')

def get_notifications(event, context):
    try:
        user_id = event.get('queryStringParameters', {}).get('user_id')
        if not user_id:
            logger.warning('Missing user_id for notifications')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'user_id is required'})
            }
        table = dynamodb.Table(NOTIFICATION_TABLE)
        response = table.query(
            IndexName='user_id-index',
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        notifications = response.get('Items', [])
        logger.info(f'Retrieved {len(notifications)} notifications for user {user_id}')
        return {
            'statusCode': 200,
            'body': json.dumps(notifications)
        }
    except Exception as e:
        logger.error(f'Get notifications error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        } 