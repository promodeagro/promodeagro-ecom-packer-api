const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, GetCommand } = require("@aws-sdk/lib-dynamodb");
require("dotenv").config();

// Initialize the DynamoDB client
const client = new DynamoDBClient({
    region: process.env.REGION || "local",
});

// Create a Document client to simplify working with DynamoDB
const docClient = DynamoDBDocumentClient.from(client);
const TableName = process.env.ORDERS_TABLE || 'Orders';
// Handler function for AWS Lambda
exports.handler = async (event) => {
    
    const orderId = event.pathParameters?.orderId;
    if (!orderId) {
        return {
            statusCode: 400,
            body: JSON.stringify({ message: "orderId is required" })
        };
    }

    try {
        const params = {
            TableName: TableName,
            Key: { id: orderId }
        };
        const command = new GetCommand(params);
        const data = await docClient.send(command)
        // Construct the response based on the provided structure
        const orderDetails = {
            OrderId: data.Item.id,
            CustomerName: data.Item.customerName,
            Payment: {
                method: data.Item.paymentDetails?.method
            },
            Price: data.Item.subTotal || 0,
            items: data.Item.items.length,
            ItemsList: data.Item.items?.map(item => ({
                Name: item.productName || "Unknown",
                Quantity: item.quantityUnits,
                Price: item.price
            })) || [],
            CostDetails: {
                SubTotal: data.Item.subTotal,
                ShippingCharges: data.Item.deliveryCharges,
                GrossDetails: data.Item.subTotal,
                TotalAmount: data.Item.totalPrice
            }
        };

        return {
            statusCode: 200,
            body: JSON.stringify(orderDetails)
        };
    } catch (error) {
        console.error("Error fetching order details:", error.stack || error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: "Error processing request",
                error: error.message || "Unknown error"
            }),
        };
    }
};
