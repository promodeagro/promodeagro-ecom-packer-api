const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();
require('dotenv').config();

exports.handler = async (event) => {
    try {
        // Get user ID from the request context (assuming it's passed in the authorizer)
        const userId = event.requestContext?.authorizer?.claims?.sub;
        
        if (!userId) {
            return {
                statusCode: 401,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({
                    message: "Unauthorized: User ID not found",
                    statusCode: 401
                })
            };
        }

        // Query notifications for the user
        const params = {
            TableName: process.env.NOTIFICATIONS_TABLE,
            KeyConditionExpression: 'UserId = :userId',
            ExpressionAttributeValues: {
                ':userId': userId
            },
            ScanIndexForward: false, // Sort in descending order (newest first)
            Limit: 50 // Limit to last 50 notifications
        };

        const result = await docClient.query(params).promise();

        // Format the response
        const notifications = result.Items.map(item => ({
            OrderId: item.OrderId,
            message: item.Message,
            timestamp: item.Timestamp,
            read: item.Read || false
        }));

        return {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify(notifications)
        };

    } catch (error) {
        console.error('Error fetching notifications:', error);
        return {
            statusCode: 500,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({
                message: "Internal Server Error",
                error: error.message
            })
        };
    }
}; 