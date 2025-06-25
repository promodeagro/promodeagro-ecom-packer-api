from dotenv import load_dotenv
load_dotenv()

# Orders Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
ORDERS_TABLE = os.environ.get('ORDERS_TABLE', 'prod-promodeagro-packerTable-orders')
ORDER_ITEMS_TABLE = os.environ.get('ORDER_ITEMS_TABLE', 'prod-promodeagro-packerTable-orderItems')

def unpacked_orders(event, context):
    try:
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.scan(
            FilterExpression=Key('status').eq('unpacked')
        )
        orders = response.get('Items', [])
        logger.info(f'Retrieved {len(orders)} unpacked orders')
        return {
            'statusCode': 200,
            'body': json.dumps(orders)
        }
    except Exception as e:
        logger.error(f'Unpacked orders error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def packed_orders(event, context):
    try:
        sort = event.get('queryStringParameters', {}).get('sort', 'desc')
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.scan(
            FilterExpression=Key('status').eq('packed')
        )
        orders = response.get('Items', [])
        orders = sorted(orders, key=lambda x: x.get('packed_at', ''), reverse=(sort=='desc'))
        logger.info(f'Retrieved {len(orders)} packed orders')
        return {
            'statusCode': 200,
            'body': json.dumps(orders)
        }
    except Exception as e:
        logger.error(f'Packed orders error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def start_order(event, context):
    try:
        order_id = event.get('pathParameters', {}).get('order_id')
        if not order_id:
            logger.warning('Missing order_id for start_order')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'order_id is required'})
            }
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        if not order:
            logger.info(f'Order not found: {order_id}')
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Order not found'})
            }
        logger.info(f'Retrieved order {order_id}')
        return {
            'statusCode': 200,
            'body': json.dumps(order)
        }
    except Exception as e:
        logger.error(f'Start order error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

def complete_order(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        order_id = body.get('order_id')
        photo = body.get('photo')
        packed_by = body.get('packed_by')
        if not order_id or not photo or not packed_by:
            logger.warning('Missing fields for complete_order')
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'order_id, photo, and packed_by are required'})
            }
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        if not order:
            logger.info(f'Order not found: {order_id}')
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Order not found'})
            }
        packed_at = '2024-01-01T00:00:00Z'  # Replace with current timestamp in production
        table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET #s = :s, packed_at = :p, packed_by = :pb, photo = :ph',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': 'packed', ':p': packed_at, ':pb': packed_by, ':ph': photo}
        )
        logger.info(f'Order {order_id} marked as packed')
        return {
            'statusCode': 200,
            'body': json.dumps({'success': True, 'order_id': order_id, 'packed_at': packed_at})
        }
    except Exception as e:
        logger.error(f'Complete order error: {str(e)}', exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        } 