import time
import uuid
from decimal import Decimal
from db_utils import (
    add_order,
    add_packer,
    assign_order,
    update_order,
    mark_order_packed,
    mark_items_not_available,
    get_order,
    get_packer
)

def print_banner(text, emoji=""):  # Centered, boxed banner
    width = 70
    banner = f"{emoji} {text} {emoji}" if emoji else text
    print("\n" + "+" + "=" * (width - 2) + "+")
    print("|" + banner.center(width - 2) + "|")
    print("+" + "=" * (width - 2) + "+\n")

def print_section(title, emoji=""):  # Centered section title
    width = 70
    section = f"{emoji} {title} {emoji}" if emoji else title
    print("\n" + section.center(width, " "))
    print("-" * width)

def print_bullets(items):
    for item in items:
        print(f"   • {item}")

def create_order_from_user():
    """
    Simulate a user placing a new order. The order starts with status 'unpacked'.
    Returns:
        str: The unique order id of the created order.
    """
    print_banner("ORDER PLACED BY USER", "📝")
    order_id = f"order-{uuid.uuid4()}"
    order = {
        "id": order_id,
        "address": {
            "address": "Test User Address",
            "addressId": str(uuid.uuid4()),
            "address_type": "Home",
            "house_number": "123",
            "landmark_area": "Test Landmark",
            "name": "TestUser",
            "phoneNumber": "1234567890",
            "userId": str(uuid.uuid4()),
            "zipCode": "500001"
        },
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "customerId": str(uuid.uuid4()),
        "customerName": "TestUser",
        "customerNameLower": "testuser",
        "customerNumber": "1234567890",
        "deliveryCharges": Decimal('20'),
        "deliverySlot": {
            "id": str(uuid.uuid4()),
            "date": time.strftime("%Y-%m-%d", time.gmtime()),
            "endAmPm": "PM",
            "endTime": "1:00",
            "shift": "morning",
            "startAmPm": "AM",
            "startTime": "10:00"
        },
        "finalTotal": Decimal('90'),
        "items": [
            {
                "category": "Fruits",
                "mrp": Decimal('95'),
                "price": Decimal('70'),
                "productId": str(uuid.uuid4()),
                "productImage": "http://example.com/apple.jpg",
                "productName": "TestApple",
                "quantity": 2,
                "quantityUnits": 1,
                "savings": Decimal('25'),
                "subCategory": "Fresh Fruits",
                "subtotal": Decimal('70'),
                "unit": "kg"
            },
            {
                "category": "Vegetables",
                "mrp": Decimal('60'),
                "price": Decimal('50'),
                "productId": str(uuid.uuid4()),
                "productImage": "http://example.com/tomato.jpg",
                "productName": "TestTomato",
                "quantity": 1,
                "quantityUnits": 1,
                "savings": Decimal('10'),
                "subCategory": "Fresh Vegetables",
                "subtotal": Decimal('50'),
                "unit": "kg"
            }
        ],
        "packedAt": None,
        "packed_by": None,
        "packerId": None,
        "paymentDetails": {
            "method": "COD",
            "status": "PENDING"
        },
        "removedItems": [],
        "savings": Decimal('35'),
        "status": "unpacked",
        "subTotal": Decimal('120'),
        "taskToken": str(uuid.uuid4()),
        "tax": Decimal('0'),
        "totalPrice": Decimal('120'),
        "totalSavings": Decimal('35.00'),
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "userId": str(uuid.uuid4()),
        "_lastChangedAt": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "_version": "1",
        "__typename": "Order"
    }
    add_order(order)
    print_section("Order Details", "📝")
    print(f"Order ID: {order['id']}")
    print(f"Status: {order['status']}")
    print(f"Customer: {order['customerName']}")
    print(f"Items:")
    for item in order['items']:
        print(f"   - {item['productName']} (Qty: {item['quantity']})")
    return order_id

def create_packer():
    """
    Create a new packer who will be assigned to the order.
    Returns:
        str: The unique packerId of the created packer.
    """
    print_banner("PACKER CREATED", "👷")
    packer_id = f"packer-{uuid.uuid4()}"
    packer = {
        "packerId": packer_id,
        "averagePackingTime": Decimal('4.5'),
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "email": f"{packer_id}@example.com",
        "firstName": "TestPacker",
        "isOnline": True,
        "lastName": "TestWorker",
        "password": "hashed_password",
        "phoneNumber": "9876543210",
        "status": "active",
        "totalOrdersPacked": 0,
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "_lastChangedAt": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())
    }
    add_packer(packer)
    print_section("Packer Details", "👷")
    print(f"Packer ID: {packer['packerId']}")
    print(f"Name: {packer['firstName']} {packer['lastName']}")
    print(f"Status: {packer['status']}")
    return packer_id

def assign_order_to_packer(order_id, packer_id):
    print_banner("ORDER ASSIGNED TO PACKER", "🤝")
    assign_order(order_id, packer_id)
    updated = get_order(order_id)
    print_section("Assignment Info", "🤝")
    print(f"Order ID: {order_id}")
    print(f"Assigned to Packer: {packer_id}")
    print(f"Status: {updated['status']}")
    return updated

def packer_check_and_process_order(order_id):
    print_banner("PACKER CHECKS ORDER", "🔍")
    order = get_order(order_id)
    unavailable_items = [order['items'][0]]
    available_items = order['items'][1:]
    if unavailable_items:
        mark_items_not_available(order_id, unavailable_items)
        print_section("Items Not Available", "🚫")
        for item in unavailable_items:
            print(f"- {item['productName']} (ID: {item['productId']})")
    if available_items:
        print_section("Available Items for Packing", "✅")
        for item in available_items:
            print(f"- {item['productName']} (ID: {item['productId']})")
        print_section("Packing Process", "📸")
        print("Taking Picture and Video of Packed Items...")
        mark_order_packed(order_id)
        update_order(order_id, {"packed_by": order['packerId'], "status": "packed"})
        print("Order status updated to 'packed'.")
    return get_order(order_id)

def assign_order_to_rider(order_id):
    print_banner("ORDER ASSIGNED TO RIDER", "🏍️")
    rider_id = f"TestRider-{uuid.uuid4()}"
    update_order(order_id, {"riderId": rider_id, "status": "assigned_to_rider"})
    print_section("Rider Assignment", "🏍️")
    print(f"Order ID: {order_id}")
    print(f"Assigned to Rider: {rider_id}")
    return get_order(order_id)

def print_journey_summary(order_id):
    print_banner("ORDER JOURNEY SUMMARY", "📋")
    order = get_order(order_id)
    packed_items = [item['productName'] for item in order.get('items', []) if item['productName'] not in [i['productName'] for i in order.get('removedItems', [])]]
    not_available_items = [item['productName'] for item in order.get('removedItems', [])]
    print_section("Final Order Status", "📦")
    print_bullets([
        f"Order ID: {order['id']}",
        f"Status: {order['status']}",
        f"Packed Items: {', '.join(packed_items) if packed_items else 'None'}",
        f"Not Available Items: {', '.join(not_available_items) if not_available_items else 'None'}",
        f"Assigned Rider: {order.get('riderId', 'None')}"
    ])

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ORDER JOURNEY START".center(70, " "))
    print("=" * 70 + "\n")
    order_id = create_order_from_user()
    packer_id = create_packer()
    assign_order_to_packer(order_id, packer_id)
    packer_check_and_process_order(order_id)
    assign_order_to_rider(order_id)
    print_journey_summary(order_id)
    print("\n" + "=" * 70)
    print("ORDER JOURNEY END".center(70, " "))
    print("=" * 70 + "\n") 