cleaimport pytest
import requests
import boto3

API_BASE = "http://localhost:3000"

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

if __name__ == "__main__":
    create_packer_table()
    create_order_table() 