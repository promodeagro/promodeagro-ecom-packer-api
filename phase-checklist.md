# Implementation Checklist: Phase 1/2/3

## 1. Authentication & Authorization
- [ ] Implement secure password hashing (replace plain text in DB)
- [ ] Add JWT or token-based authentication (currently disabled)
- [ ] Enforce authorization checks in all handlers
- [ ] Implement login endpoint as per OpenAPI spec
- [ ] Implement forgot password flow (send OTP)
- [ ] Implement OTP verification endpoint
- [ ] Implement password reset endpoint
- [ ] Implement logout endpoint

## 2. User Profile Management
- [ ] Implement get profile endpoint
- [ ] Implement update profile endpoint
- [ ] Implement change password endpoint
- [ ] Validate all profile input fields
- [ ] Add profile image upload support (if in PRD)

## 3. Orders Management
- [ ] Implement unpacked orders listing
- [ ] Implement packed orders listing
- [ ] Implement start order (fetch order details)
- [ ] Implement complete order (mark as packed, upload photo)
- [ ] Implement get completed order details
- [ ] Validate order status transitions (unpacked → packed)
- [ ] Add timestamps and packed_by fields correctly
- [ ] Handle payment status and cost details as per spec

## 4. Notifications
- [ ] Implement get notifications endpoint
- [ ] Ensure notifications are filtered by user_id
- [ ] Add notification creation logic (on order events)
- [ ] Mark notifications as read (if in PRD)

## 5. API & Data Validation
- [ ] Validate all incoming request bodies against OpenAPI spec
- [ ] Return proper error codes and messages for invalid input
- [ ] Add input sanitization to prevent injection attacks

## 6. Testing & QA
- [ ] Write/expand pytest tests for all endpoints
- [ ] Add tests for authentication edge cases
- [ ] Add tests for order status transitions
- [ ] Add tests for notification retrieval

## 7. Deployment & Environment
- [ ] Ensure all environment variables are loaded and documented
- [ ] Add deployment scripts for AWS Lambda
- [ ] Test serverless offline and AWS deployment flows 