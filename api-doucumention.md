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
            "OrderStatus": "delivered"
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
    "OrderId": "401-3680557-6464026",
    "CustomerName": "sukanta halder",
    "Payment": {
        "method": "cash"
    },
    "Price": 122,
    "items": 2,
    "ItemsList": [
        {
            "Name": "Dragon fruit red",
            "Quantity": 1,
            "Price": 60
        },
        {
            "Name": "Cucumber",
            "Quantity": 250,
            "Price": 2
        }
    ],
    "CostDetails": {
        "SubTotal": 122,
        "ShippingCharges": 0,
        "GrossDetails": 122,
        "TotalAmount": "122.00"
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
  "userId": "0076c700-adc1-49d0-bd60-f97d77c9e688",
  "userName": "sukanta halder",
  "email": "haldersukanta372@gmail.com",
  "newPassword": "Sukanta@546"
}
```
## Responce 200
```json
{
    "message": "Password changed successfully.",
    "statusCode": 200
}

```