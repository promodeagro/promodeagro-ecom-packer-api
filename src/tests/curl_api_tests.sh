#!/bin/bash

API_BASE="http://localhost:3000/dev"

# Authentication

echo "\n=== LOGIN ==="
curl -s -X POST $API_BASE/login \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@example.com", "password": "testpassword"}' | jq

echo "\n=== FORGOT PASSWORD ==="
curl -s -X POST $API_BASE/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@example.com"}' | jq

echo "\n=== VERIFY OTP ==="
curl -s -X POST $API_BASE/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@example.com", "otp": "123456"}' | jq

echo "\n=== RESET PASSWORD ==="
curl -s -X POST $API_BASE/reset-password \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@example.com", "new_password": "newpass", "confirm_password": "newpass"}' | jq

echo "\n=== LOGOUT ==="
curl -s -X POST $API_BASE/logout | jq

# Profile
echo "\n=== GET PROFILE ==="
curl -s -X GET "$API_BASE/profile?email=testuser@example.com" | jq

echo "\n=== UPDATE PROFILE ==="
curl -s -X POST $API_BASE/profile/update \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@example.com", "username": "TestUser"}' | jq

echo "\n=== CHANGE PASSWORD ==="
curl -s -X POST $API_BASE/profile/change-password \
  -H "Content-Type: application/json" \
  -d '{"email": "testuser@example.com", "current_password": "oldpass", "new_password": "newpass", "confirm_password": "newpass"}' | jq

# Notifications
echo "\n=== GET NOTIFICATIONS ==="
curl -s -X GET "$API_BASE/notifications?user_id=test-user-001" | jq

# Orders
echo "\n=== GET UNPACKED ORDERS ==="
curl -s -X GET $API_BASE/orders/unpacked | jq

echo "\n=== GET PACKED ORDERS ==="
curl -s -X GET $API_BASE/orders/packed | jq

# Order Journey
echo "\n=== CREATE ORDER ==="
ORDER_ID=$(curl -s -X POST $API_BASE/orders \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | tee /dev/tty | jq -r '.order_id')

echo "\n=== ASSIGN PACKER ==="
curl -s -X POST $API_BASE/orders/$ORDER_ID/assign-packer \
  -H "Content-Type: application/json" \
  -d '{"packer_id": "packer-001"}' | jq

echo "\n=== MARK ITEMS UNAVAILABLE ==="
curl -s -X POST $API_BASE/orders/$ORDER_ID/mark-items-unavailable \
  -H "Content-Type: application/json" \
  -d '{"items": ["prod-001"]}' | jq

echo "\n=== ASSIGN RIDER ==="
curl -s -X POST $API_BASE/orders/$ORDER_ID/assign-rider \
  -H "Content-Type: application/json" \
  -d '{"rider_id": "rider-001"}' | jq 