import pytest
import requests
import boto3

API_BASE = "http://localhost:3000/dev"

@pytest.mark.parametrize("payload,expected_key", [
    ( {"email": "testuser@example.com", "password": "testpassword"}, "user_id" ),
])
def test_login(payload, expected_key):
    resp = requests.post(f"{API_BASE}/login", json=payload)
    print("/login response:", resp.json())
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        assert expected_key in resp.json()
    else:
        assert "message" in resp.json()

def test_forgot_password():
    payload = {"email": "testuser@example.com"}
    resp = requests.post(f"{API_BASE}/forgot-password", json=payload)
    print("/forgot-password response:", resp.json())
    assert resp.status_code in (200, 404)
    assert "message" in resp.json()

def test_verify_otp():
    payload = {"email": "testuser@example.com", "otp": "123456"}
    resp = requests.post(f"{API_BASE}/verify-otp", json=payload)
    print("/verify-otp response:", resp.json())
    assert resp.status_code in (200, 401)
    assert "message" in resp.json()

def test_reset_password():
    payload = {"email": "testuser@example.com", "new_password": "newpass", "confirm_password": "newpass"}
    resp = requests.post(f"{API_BASE}/reset-password", json=payload)
    print("/reset-password response:", resp.json())
    assert resp.status_code in (200, 400, 404)
    assert "message" in resp.json()

def test_logout():
    resp = requests.post(f"{API_BASE}/logout")
    print("/logout response:", resp.json())
    assert resp.status_code == 200
    assert "message" in resp.json()

def test_get_profile():
    params = {"email": "testuser@example.com"}
    resp = requests.get(f"{API_BASE}/profile", params=params)
    print("/profile response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    # If found, should have at least 'email' or 'user_id' or 'message'
    assert any(k in resp.json() for k in ("email", "user_id", "message"))

def test_update_profile():
    payload = {"email": "testuser@example.com", "username": "TestUser"}
    resp = requests.post(f"{API_BASE}/profile/update", json=payload)
    print("/profile/update response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    assert "message" in resp.json()

def test_change_password():
    payload = {"email": "testuser@example.com", "current_password": "oldpass", "new_password": "newpass", "confirm_password": "newpass"}
    resp = requests.post(f"{API_BASE}/profile/change-password", json=payload)
    print("/profile/change-password response:", resp.json())
    assert resp.status_code in (200, 400)
    assert "message" in resp.json()

def test_orders_unpacked():
    resp = requests.get(f"{API_BASE}/orders/unpacked")
    print("/orders/unpacked response:", resp.json())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_orders_packed():
    resp = requests.get(f"{API_BASE}/orders/packed")
    print("/orders/packed response:", resp.json())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_orders_start():
    order_id = "test-order-001"
    resp = requests.get(f"{API_BASE}/orders/start/{order_id}")
    print(f"/orders/start/{{order_id}} response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    assert isinstance(resp.json(), dict)

def test_orders_complete():
    payload = {"order_id": "test-order-001", "photo": "url", "packed_by": "packer-001"}
    resp = requests.post(f"{API_BASE}/orders/complete", json=payload)
    print("/orders/complete response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    assert isinstance(resp.json(), dict)

def test_notifications():
    params = {"user_id": "test-user-001"}
    resp = requests.get(f"{API_BASE}/notifications", params=params)
    print("/notifications response:", resp.json())
    assert resp.status_code in (200, 400)
    assert isinstance(resp.json(), list) or "message" in resp.json() 

import boto3

dynamodb = boto3.resource('dynamodb', region_name='your-region')
order_table = dynamodb.Table('Order')
packer_table = dynamodb.Table('Packer')

def add_packer(packer):
    packer_table.put_item(Item=packer)

def add_order(order):
    order_table.put_item(Item=order)

def get_order(order_id):
    return order_table.get_item(Key={'id': order_id}).get('Item')

def get_packer(packer_id):
    return packer_table.get_item(Key={'id': packer_id}).get('Item')

def test_create_order():
    payload = {
        "address": {"address": "123 Test St", "userId": "user-001"},
        "customerId": "user-001",
        "customerName": "Test User",
        "customerNumber": "1234567890",
        "deliveryCharges": 10,
        "deliverySlot": {"id": "slot-001", "date": "2024-01-01"},
        "finalTotal": 100,
        "items": [
            {"productId": "prod-001", "productName": "Apple", "quantity": 2, "price": 50},
            {"productId": "prod-002", "productName": "Banana", "quantity": 1, "price": 20}
        ],
        "paymentDetails": {"method": "COD", "status": "PENDING"},
        "savings": 5,
        "subTotal": 120,
        "tax": 0,
        "totalPrice": 120,
        "totalSavings": 5,
        "userId": "user-001"
    }
    resp = requests.post(f"{API_BASE}/orders", json=payload)
    print("/orders (create) response:", resp.json())
    assert resp.status_code in (201, 200)
    data = resp.json()
    assert "order_id" in data or "order" in data
    # Return order_id for chaining
    return data.get("order_id") or data["order"]["order_id"]

def test_assign_packer():
    order_id = test_create_order()
    payload = {"packer_id": "packer-001"}
    resp = requests.post(f"{API_BASE}/orders/{order_id}/assign-packer", json=payload)
    print(f"/orders/{{order_id}}/assign-packer response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    data = resp.json()
    assert "order_id" in data and "packer_id" in data
    return order_id

def test_mark_items_unavailable():
    order_id = test_create_order()
    # Mark the first item as unavailable
    items_to_remove = ["prod-001"]
    payload = {"items": items_to_remove}
    resp = requests.post(f"{API_BASE}/orders/{order_id}/mark-items-unavailable", json=payload)
    print(f"/orders/{{order_id}}/mark-items-unavailable response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    data = resp.json()
    assert "order_id" in data and "removed_items" in data
    return order_id

def test_assign_rider():
    order_id = test_create_order()
    payload = {"rider_id": "rider-001"}
    resp = requests.post(f"{API_BASE}/orders/{order_id}/assign-rider", json=payload)
    print(f"/orders/{{order_id}}/assign-rider response:", resp.json())
    assert resp.status_code in (200, 404, 400)
    data = resp.json()
    assert "order_id" in data and "rider_id" in data
    return order_id

if __name__ == "__main__":
    create_packer_table()
    create_order_table() 