import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

def create_packer_table():
    """
    Creates the 'Packer' table in DynamoDB with 'packerId' as the partition key.
    Usage: Call once during setup. Waits until the table exists.
    """
    try:
        table = dynamodb.create_table(
            TableName='Packer',
            KeySchema=[{'AttributeName': 'packerId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'packerId', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print("Packer table created.")
    except ClientError as e:
        print(f"Error creating Packer table: {e}")

def create_order_table():
    """
    Creates the 'Order' table in DynamoDB with 'id' as the partition key.
    Usage: Call once during setup. Waits until the table exists.
    """
    try:
        table = dynamodb.create_table(
            TableName='Order',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print("Order table created.")
    except ClientError as e:
        print(f"Error creating Order table: {e}")

def add_packer(packer):
    """
    Adds a new packer to the 'Packer' table.
    Args:
        packer (dict): Dictionary containing packer details. Must include 'packerId'.
    Usage: add_packer({...})
    """
    table = dynamodb.Table('Packer')
    try:
        table.put_item(Item=packer)
        print(f"Packer {packer['packerId']} added.")
    except ClientError as e:
        print(f"Error adding packer: {e}")

def add_order(order):
    """
    Adds a new order to the 'Order' table.
    Args:
        order (dict): Dictionary containing order details. Must include 'id'.
    Usage: add_order({...})
    """
    table = dynamodb.Table('Order')
    try:
        table.put_item(Item=order)
        print(f"Order {order['id']} added.")
    except ClientError as e:
        print(f"Error adding order: {e}")

def get_packer(packer_id):
    """
    Retrieves a packer from the 'Packer' table by packerId.
    Args:
        packer_id (str): The packerId of the packer to retrieve.
    Returns:
        dict or None: The packer item if found, else None.
    Usage: get_packer('test-pytest-packer-001')
    """
    table = dynamodb.Table('Packer')
    try:
        response = table.get_item(Key={'packerId': packer_id})
        return response.get('Item')
    except ClientError as e:
        print(f"Error retrieving packer: {e}")
        return None

def get_order(order_id):
    """
    Retrieves an order from the 'Order' table by ID.
    Args:
        order_id (str): The ID of the order to retrieve.
    Returns:
        dict or None: The order item if found, else None.
    Usage: get_order('401-3760341')
    """
    table = dynamodb.Table('Order')
    try:
        response = table.get_item(Key={'id': order_id})
        return response.get('Item')
    except ClientError as e:
        print(f"Error retrieving order: {e}")
        return None

def assign_order(order_id, packer_id):
    """
    Assigns an order to a packer by updating the packerId field of the order.
    Args:
        order_id (str): The ID of the order to assign.
        packer_id (str): The packerId to assign the order to.
    Returns:
        bool: True if update was successful, False otherwise.
    """
    table = dynamodb.Table('Order')
    try:
        table.update_item(
            Key={'id': order_id},
            UpdateExpression="SET packerId = :pid",
            ExpressionAttributeValues={':pid': packer_id}
        )
        print(f"Order {order_id} assigned to packer {packer_id}.")
        return True
    except ClientError as e:
        print(f"Error assigning order: {e}")
        return False

def mark_order_packed(order_id):
    """
    Marks an order as packed by updating its status to 'packed'.
    Args:
        order_id (str): The ID of the order to mark as packed.
    Returns:
        bool: True if update was successful, False otherwise.
    """
    table = dynamodb.Table('Order')
    try:
        table.update_item(
            Key={'id': order_id},
            UpdateExpression="SET #s = :packed",
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':packed': 'packed'}
        )
        print(f"Order {order_id} marked as packed.")
        return True
    except ClientError as e:
        print(f"Error marking order as packed: {e}")
        return False

def update_order(order_id, update_fields):
    """
    Updates fields of an order in the 'Order' table.
    Args:
        order_id (str): The ID of the order to update.
        update_fields (dict): Dictionary of fields to update.
    Returns:
        bool: True if update was successful, False otherwise.
    """
    table = dynamodb.Table('Order')
    try:
        # Handle reserved keywords
        reserved_keywords = {'status', 'order', 'user', 'type'}
        expr_attr_names = {}
        update_expr_parts = []
        expr_attr_vals = {}
        for k, v in update_fields.items():
            if k in reserved_keywords:
                expr_attr_names[f"#{k}"] = k
                update_expr_parts.append(f"#{k} = :{k}")
            else:
                update_expr_parts.append(f"{k} = :{k}")
            expr_attr_vals[f":{k}"] = v
        update_expr = "SET " + ", ".join(update_expr_parts)
        kwargs = {
            'Key': {'id': order_id},
            'UpdateExpression': update_expr,
            'ExpressionAttributeValues': expr_attr_vals
        }
        if expr_attr_names:
            kwargs['ExpressionAttributeNames'] = expr_attr_names
        table.update_item(**kwargs)
        print(f"Order {order_id} updated with {update_fields}.")
        return True
    except ClientError as e:
        print(f"Error updating order: {e}")
        return False

def mark_items_not_available(order_id, items):
    """
    Marks items as not available in an order by updating the removedItems field.
    Args:
        order_id (str): The ID of the order.
        items (list): List of items to mark as not available.
    Returns:
        bool: True if update was successful, False otherwise.
    """
    table = dynamodb.Table('Order')
    try:
        table.update_item(
            Key={'id': order_id},
            UpdateExpression="SET removedItems = :items",
            ExpressionAttributeValues={':items': items}
        )
        print(f"Order {order_id} items marked as not available: {items}")
        return True
    except ClientError as e:
        print(f"Error marking items not available: {e}")
        return False 