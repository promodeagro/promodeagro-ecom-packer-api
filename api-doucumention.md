# PROMODEAGRO-ECOM-PACKER-API DOCUMENTATION


<br>
<br>


# home

## API Endpoint: UnpackedOrders

This endpoint is used to UnpackedOrders.

## Method

- **Method**: GET

## URL

- **URL**: `http://localhost:3000/dev/getAllUnpackedOrders`

## Content-Type

- **Content-Type**: `application/json`

## Responce

```json
"TotalUnpackedOrders": 53,
    "UnpackedOrders": [
        {
            "OrderId": "401-3680557-6464026",
            "CustomerName": "umran",
            "TotalItems": 1,
            "OrderStatus": "order placed"
        }
    ]
```
## API Endpoint: PackedOrders

This endpoint is used to PackedOrders.

## Method

- **Method**: GET

## URL

- **URL**: `http://localhost:3000/dev/getAllPackedOrders`

## Content-Type

- **Content-Type**: `application/json`

## Responce

```json
"TotalPackedOrders": 7,
    [
        {
            "OrderId": "401-3680557-6464026",
            "CustomerName": "sukanta halder",
            "TotalItems": 2,
            "OrderStatus": "Packed"
        }
    ]
```
## API Endpoint: OrderDetails

This endpoint is used to OrderDetails.

## Method

- **Method**: GET

## URL

- **URL**: `http://localhost:3000/dev/OrderDetails/{orderId}`

## Content-Type

- **Content-Type**: `application/json`

## Responce

```json
{
    "OrderId": "401-1070431-1348467",
    "CustomerName": "sukanta halder",
    "Payment": {
        "method": "cash"
    },
    "Price": 208,
    "items": 5,
    "ItemsList": [
        {
            "Name": "Cauliflower",
            "Quantity": 1,
            "Price": 25,
            "Images": "https://ecomdmsservice.s3.amazonaws.com/Product-images/1726328242139-Cauliflower.jpg"
        },
        {
            "Name": "Cucumber",
            "Quantity": 250,
            "Price": 8,
            "Images": "https://ecomdmsservice.s3.amazonaws.com/Product-images/1726328245471-cucumber.jpg"
        },
        {
            "Name": "Kolkata bagun",
            "Quantity": 250,
            "Price": 25,
            "Images": "https://ecomdmsservice.s3.amazonaws.com/Product-images/1726328255821-kolkata-bringile.png"
        },
        {
            "Name": "Red Capsicum",
            "Quantity": 1,
            "Price": 120,
            "Images": [
                "https://prod-promodeargo-admin-api-mediabucket46c59097-tynsj9joexji.s3.us-east-1.amazonaws.com/Q%EF%BF%BD%EF%BF%BD3%3A%EF%BF%BD%EF%BF%BD%2C%EF%BF%BD%EF%BF%BD%EF%BF%BD%EF%BF%BD3d%EF%BF%BD7Red%20Capsicum.jpeg"
            ]
        },
        {
            "Name": "Strawberry",
            "Quantity": 250,
            "Price": 30,
            "Images": "https://ecomdmsservice.s3.amazonaws.com/Product-images/1726328276860-strawberry.jpg"
        }
    ],
    "CostDetails": {
        "SubTotal": 208,
        "ShippingCharges": 0,
        "GrossDetails": 208,
        "TotalAmount": "208.00"
    }
}
```

## API Endpoint: UploadPackingPhoto

This endpoint is used to UploadPackingPhoto.

## Method

- **Method**: POST

## URL

- **URL**: `http://localhost:3000/dev/orders/{orderId}/upload-photo`

## Content-Type

- **Content-Type**: `application/json`

## Request Body

The request body should be a JSON object with the following fields:

```json
{
  "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAYkAAAFqCAYAAADvDaaRAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAP+lSURBVHhe7P35s2RbdpiHrbw5552rbs3Dm6fuBhpDEyQFEYBlKhgM6y+xrR9sS4pgiGJDsk0qNNkKhyzSQ1hhywxKMklNZJAESZEYCDSAbnSjpzfXe/VqrrrzvTnfTH/f2nmq6nX3IxsSRin3rVOZec4e1l57zXs4tdlsNo9lWqZlWqZlWqYfkFYWn8u0TMu0TMu0TN+XlkpimZZpmZZpmT4zLZXEMi3TMi3TMn1mWiqJZVqmZVqmZfrMtFQSy7RMy7RMy/"
}
```

## Responce 200
```json
{
    "photoUrl": "https://ecomdmsservice.s3.amazonaws.com/Product-images/",
    "OrderId": "401-3098942-1142539"
}

```

## API Endpoint: CompletePackOrder

This endpoint is used to CompletePackOrder.

## Method

- **Method**: PUT

## URL

- **URL**: `http://localhost:3000/dev/orders/{orderId}/CompletePacked`

## Content-Type

- **Content-Type**: `application/json`

## Request Body

The request body should be a JSON object with the following fields:

```json
{
    "Status":"Packed"
}
```
## Responce 200
```json
{
    "message": "Order id 5300951 has been Packed successfully"
}
```
# profile-details
## API Endpoint: updatePassword

This endpoint is used to updatePassword.

## Method

- **Method**: POST

## URL

- **URL**: `http://localhost:3000/dev/updatePassword`

## Content-Type

- **Content-Type**: `application/json`

## Request Body

The request body should be a JSON object with the following fields:

```json
{
  "userId": "41b554ce-a17e-4c3f-9b16-45a255054909",
  "userName": "sukanta halder",
  "email": "haldersukanta372@gmail.com",
  "oldPassword": "Sukanta@85370",
  "newPassword": "Sukanta@853701"
}
```
## Responce 200
```json
{
    "message": "Password changed successfully.",
    "statusCode": 200
}

```