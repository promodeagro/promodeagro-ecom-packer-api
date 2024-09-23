const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, ScanCommand } = require("@aws-sdk/lib-dynamodb");
require("dotenv").config();

// Initialize the DynamoDB client
const client = new DynamoDBClient({
    region: process.env.REGION || "us-east-1",
});
const docClient = DynamoDBDocumentClient.from(client);
const TableName = process.env.ORDERS_TABLE || 'Orders';

exports.handler = async (event) => {
    console.log("Event received:", JSON.stringify(event));
    try {
        const params = {
            TableName: TableName,
            FilterExpression: "#status = :status",
            ExpressionAttributeNames: {
                "#status": "status" 
            },
            ExpressionAttributeValues: {
                ":status": "order placed" 
            }
        };
        const command = new ScanCommand(params);
        const data = await docClient.send(command);
        if (!data.Items || data.Items.length === 0) {
            console.log("No packed orders found");
            return {
                statusCode: 200,
                body: JSON.stringify({
                    TotalPackedOrders: 0
                })
            };
        }

        // Example aggregation logic to collect all packed orders
        const result = data.Items.map(item => ({
            OrderId: item.id,
            CustomerName: item.customerName,
            TotalItems: Array.isArray(item.items) ? item.items.length : 0,
            OrderStatus: item.status
        }));

        return {
            statusCode: 200,
            body: JSON.stringify({
                TotalUnpackedOrders: result.length,
                UnpackedOrders: result
            })
        };
    } catch (error) {
        console.error("Error processing request:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: "Error processing request",
                error: error.message
            }),
        };
    }
};