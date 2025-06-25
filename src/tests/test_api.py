import requests

BASE_URL = 'http://localhost:3000/dev'

def test_login():
    resp = requests.post(f'{BASE_URL}/login', json={
        'email': 'user@example.com',
        'password': 'Test@1234'
    })
    assert resp.status_code == 200
    data = resp.json()
    assert 'token' in data
    assert 'user_id' in data

def test_forgot_password():
    resp = requests.post(f'{BASE_URL}/forgot-password', json={
        'email': 'user@example.com'
    })
    assert resp.status_code in (200, 404)

def test_verify_otp():
    resp = requests.post(f'{BASE_URL}/verify-otp', json={
        'email': 'user@example.com',
        'otp': '123456'  # Replace with actual OTP if needed
    })
    assert resp.status_code in (200, 401)

def test_reset_password():
    resp = requests.post(f'{BASE_URL}/reset-password', json={
        'email': 'user@example.com',
        'new_password': 'NewPass@123',
        'confirm_password': 'NewPass@123'
    })
    assert resp.status_code in (200, 400, 404)

def test_get_unpacked_orders():
    resp = requests.get(f'{BASE_URL}/orders/unpacked')
    assert resp.status_code == 200

def test_get_notifications():
    resp = requests.get(f'{BASE_URL}/notifications', params={'user_id': 'user1'})
    assert resp.status_code == 200

def test_get_profile():
    resp = requests.get(f'{BASE_URL}/profile', params={'user_id': 'user1'})
    assert resp.status_code in (200, 404) 