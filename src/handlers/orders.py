# IGNORE AUTH: Authorization checks are disabled for development/testing in this file. All endpoints are public.
from dotenv import load_dotenv
load_dotenv()

# Orders Handlers

import os
import json
import logging
import boto3
from boto3.dynamodb.conditions import Key
from src.commonfunctions.utils import require_auth
from src.commonfunctions.utils import format_response
from src.commonfunctions.utils import convert_decimal

import uuid
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
ORDERS_TABLE = os.environ.get('ORDERS_TABLE', 'prod-promodeagro-packerTable-orders')
ORDER_ITEMS_TABLE = os.environ.get('ORDER_ITEMS_TABLE', 'prod-promodeagro-packerTable-orderItems')

# IGNORE TOKEN: Token logic is disabled for development/testing
def unpacked_orders(event, context):
    try:
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.scan(
            FilterExpression=Key('status').eq('unpacked')
        )
        orders = response.get('Items', [])
        orders = convert_decimal(orders)
        # Map fields for frontend
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                "order_id": order.get("order_id"),
                "customer_name": order.get("customerName"),
                "total_items": len(order.get("items", [])),
                "status": order.get("status"),
                "packed_by": order.get("packed_by", ""),
                "packed_at": order.get("packed_at", order.get("packedAt", "")),
                "created_at": order.get("created_at", order.get("createdAt", "")),
                "price": order.get("price", order.get("totalPrice", "")),
                "payment_method": order.get("payment_method", order.get("paymentDetails", {}).get("method") if isinstance(order.get("paymentDetails"), dict) else ""),
                # Add more fields as needed
            })
        logger.info(f'Retrieved {len(formatted_orders)} unpacked orders')
        return format_response(200, formatted_orders)
    except Exception as e:
        logger.error(f'Unpacked orders error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

# IGNORE TOKEN: Token logic is disabled for development/testing
def packed_orders(event, context):
    try:
        query_params = event.get('queryStringParameters') or {}
        sort = query_params.get('sort', 'desc')
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.scan(
            FilterExpression=Key('status').eq('packed')
        )
        orders = response.get('Items', [])
        orders = convert_decimal(orders)
        orders = sorted(orders, key=lambda x: x.get('packed_at', ''), reverse=(sort=='desc'))
        logger.info(f'Retrieved {len(orders)} packed orders')
        return format_response(200, orders)
    except Exception as e:
        logger.error(f'Packed orders error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

# IGNORE TOKEN: Token logic is disabled for development/testing
def start_order(event, context):
    try:
        order_id = event.get('pathParameters', {}).get('order_id')
        if not order_id:
            logger.warning('Missing order_id for start_order')
            return format_response(400, {'message': 'order_id is required'})
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        order = convert_decimal(order)
        if not order:
            logger.info(f'Order not found: {order_id}')
            return format_response(404, {'message': 'Order not found'})
        # Map fields for frontend
        items = [
            {
                "name": item.get("productName", ""),
                "quantity": item.get("quantity", 0),
                "price": item.get("price", 0),
                "image": item.get("productImage", ""),
                "sku": item.get("productId", "")
            }
            for item in order.get("items", [])
        ]
        cost_details = {
            "sub_total": order.get("subTotal", 0),
            "shipping_charges": order.get("deliveryCharges", 0),
            "tax": order.get("tax", 0),
            "discount": order.get("savings", 0),
            "total_amount": order.get("totalPrice", 0),
            "total_savings": order.get("totalSavings", 0)
        }
        result = {
            "order_id": order.get("order_id"),
            "customer_name": order.get("customerName", ""),
            "total_items": len(items),
            "status": order.get("status", ""),
            "packed_by": order.get("packed_by", ""),
            "packed_at": order.get("packed_at", order.get("packedAt", "")),
            "created_at": order.get("created_at", order.get("createdAt", "")),
            "price": order.get("price", order.get("totalPrice", 0)),
            "payment_method": order.get("payment_method", order.get("paymentDetails", {}).get("method") if isinstance(order.get("paymentDetails"), dict) else ""),
            "photo": order.get("photo", ""),
            "items": items,
            "cost_details": cost_details
        }
        logger.info(f'Retrieved order {order_id}')
        return format_response(200, result)
    except Exception as e:
        logger.error(f'Start order error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

# IGNORE TOKEN: Token logic is disabled for development/testing
def complete_order(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        order_id = body.get('order_id')
        photo = body.get('photo')
        packed_by = body.get('packed_by')
        if not order_id or not photo or not packed_by:
            logger.warning('Missing fields for complete_order')
            return format_response(400, {'message': 'order_id, photo, and packed_by are required'})
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        if not order:
            logger.info(f'Order not found: {order_id}')
            return format_response(404, {'message': 'Order not found'})
        packed_at = '2024-01-01T00:00:00Z'  # Replace with current timestamp in production
        table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET #s = :s, packed_at = :p, packed_by = :pb, photo = :ph',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':s': 'packed', ':p': packed_at, ':pb': packed_by, ':ph': photo}
        )
        logger.info(f'Order {order_id} marked as packed')
        return format_response(200, {'success': True, 'order_id': order_id, 'packed_at': packed_at})
    except Exception as e:
        logger.error(f'Complete order error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

# IGNORE TOKEN: Token logic is disabled for development/testing
def get_completed_order_details(event, context):
    try:
        order_id = event.get('pathParameters', {}).get('order_id')
        if not order_id:
            logger.warning('Missing order_id for get_completed_order_details')
            return format_response(400, {'message': 'order_id is required'})
        table = dynamodb.Table(ORDERS_TABLE)
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        order = convert_decimal(order)
        if not order:
            logger.info(f'Order not found: {order_id}')
            return format_response(404, {'message': 'Order not found'})
        # Ensure the order is packed/completed
        if order.get('status') != 'packed':
            logger.info(f'Order {order_id} is not packed/completed')
            return format_response(400, {'message': 'Order is not completed'})
        # Map fields for frontend
        result = {
            "order_id": order.get("order_id"),
            "customer_name": order.get("customerName"),
            "total_items": len(order.get("items", [])),
            "status": order.get("status"),
            "packed_by": order.get("packed_by", ""),
            "packed_at": order.get("packed_at", order.get("packedAt", "")),
            "created_at": order.get("created_at", order.get("createdAt", "")),
            "price": order.get("price", order.get("totalPrice", "")),
            "payment_method": order.get("payment_method", order.get("paymentDetails", {}).get("method") if isinstance(order.get("paymentDetails"), dict) else ""),
            # Add more fields as needed
        }
        logger.info(f'Retrieved completed order details for {order_id}')
        return format_response(200, result)
    except Exception as e:
        logger.error(f'Get completed order details error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def create_order(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        order_id = body.get('order_id') or f"order-{str(uuid.uuid4())}"
        order = body.copy()
        order['order_id'] = order_id
        order['status'] = 'unpacked'
        order['created_at'] = order.get('created_at') or time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
        order['removedItems'] = []
        table = dynamodb.Table(ORDERS_TABLE)
        table.put_item(Item=order)
        logger.info(f'Order created: {order_id}')
        return format_response(201, {'message': 'Order created', 'order_id': order_id, 'order': order})
    except Exception as e:
        logger.error(f'Create order error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def assign_packer(event, context):
    try:
        order_id = event.get('pathParameters', {}).get('order_id')
        body = json.loads(event.get('body', '{}'))
        packer_id = body.get('packer_id')
        table = dynamodb.Table(ORDERS_TABLE)
        # Update order with packer_id, keep status as unpacked
        table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET packer_id = :p, #s = :s',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':p': packer_id, ':s': 'unpacked'}
        )
        logger.info(f'Order {order_id} assigned to packer {packer_id}')
        return format_response(200, {'message': 'Order assigned to packer', 'order_id': order_id, 'packer_id': packer_id})
    except Exception as e:
        logger.error(f'Assign packer error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def mark_items_unavailable(event, context):
    try:
        order_id = event.get('pathParameters', {}).get('order_id')
        body = json.loads(event.get('body', '{}'))
        items_to_remove = body.get('items', [])
        table = dynamodb.Table(ORDERS_TABLE)
        # Get current order
        response = table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        if not order:
            return format_response(404, {'message': 'Order not found'})
        items = order.get('items', [])
        removed_items = order.get('removedItems', [])
        # Move items from items to removedItems
        new_items = [item for item in items if item.get('productId') not in items_to_remove]
        new_removed = removed_items + [item for item in items if item.get('productId') in items_to_remove]
        table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET #i = :i, removedItems = :r',
            ExpressionAttributeNames={'#i': 'items'},
            ExpressionAttributeValues={':i': new_items, ':r': new_removed}
        )
        logger.info(f'Order {order_id}: marked items unavailable: {items_to_remove}')
        return format_response(200, {'message': 'Items marked as not available', 'order_id': order_id, 'removed_items': items_to_remove})
    except Exception as e:
        logger.error(f'Mark items unavailable error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)})

def assign_rider(event, context):
    try:
        order_id = event.get('pathParameters', {}).get('order_id')
        body = json.loads(event.get('body', '{}'))
        rider_id = body.get('rider_id')
        table = dynamodb.Table(ORDERS_TABLE)
        # Update order with rider_id and status
        table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET rider_id = :r, #s = :s',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':r': rider_id, ':s': 'assigned_to_rider'}
        )
        logger.info(f'Order {order_id} assigned to rider {rider_id}')
        return format_response(200, {'message': 'Order assigned to rider', 'order_id': order_id, 'rider_id': rider_id})
    except Exception as e:
        logger.error(f'Assign rider error: {str(e)}', exc_info=True)
        return format_response(500, {'message': 'Internal server error', 'error': str(e)}) 