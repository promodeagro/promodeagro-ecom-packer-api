# PROMODEAGRO-ECOM-PACKER-API DOCUMENTATION


<br>
<br>


# home

## API Endpoint: UnpackedOrders

This endpoint is used to unpacked-order.

## Method

- **Method**: GET

## URL

- **URL**: `http://localhost:3000/dev/Unpacked-Orders`

## Content-Type

- **Content-Type**: `application/json`

## Responce

```json
"TotalUnpackedOrders": 53,
    "UnpackedOrders": [
        {
            "OrderId": "401-1064274-2080780",
            "CustomerName": "Mr",
            "TotalItems": 2,
            "OrderStatus": "delivered"
        }
    ]
```
## API Endpoint: PackedOrders

This endpoint is used to PackedOrders.

## Method

- **Method**: GET

## URL

- **URL**: `http://localhost:3000/dev/Packed-Orders`

## Content-Type

- **Content-Type**: `application/json`

## Responce

```json
"TotalPackedOrders": 7,
    [
        {
            "OrderId": "401-7048483-3423372",
            "CustomerName": "umran",
            "TotalItems": 1,
            "OrderStatus": "Packed"
        }
    ]
```
## API Endpoint: OrderDetails

This endpoint is used to OrderDetails.

## Method

- **Method**: GET

## URL

- **URL**: `http://localhost:3000/dev/orders/{orderId}`

## Content-Type

- **Content-Type**: `application/json`

## Responce

```json
{
    "OrderId": "401-3680557-6464026",
    "CustomerName": "sukanta halder",
    "Payment": {
        "method": "cash"
    },
    "Price": 90,
    "items": 2,
    "ItemsList": [
        {
            "Name": "Dragon fruit red",
            "Quantity": 1,
            "Price": 60
        },
        {
            "Name": "Strawberry",
            "Quantity": 250,
            "Price": 30
        }
    ],
    "CostDetails": {
        "SubTotal": 90,
        "ShippingCharges": 0,
        "GrossDetails": 90,
        "TotalAmount": "90.00"
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

## API Endpoint: CompletePackOrder

This endpoint is used to CompletePackOrder.

## Method

- **Method**: PUT

## URL

- **URL**: `http://localhost:3000/dev/orders/{orderId}/complete`

## Content-Type

- **Content-Type**: `application/json`

## Request Body

The request body should be a JSON object with the following fields:

```json
{
    "Status":"Packed"
}
```