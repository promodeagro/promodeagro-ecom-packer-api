const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, UpdateCommand, GetCommand } = require("@aws-sdk/lib-dynamodb");
const AWS = require("aws-sdk");

const client = new DynamoDBClient({
    region: process.env.REGION || "us-east-1"
});
const docClient = DynamoDBDocumentClient.from(client);
const TableName = process.env.ORDERS_TABLE || 'Orders';
const stepfunctions = new AWS.StepFunctions();
const orderProcessSFArn = 'arn:aws:states:us-east-1:851725323791:stateMachine:OrderTrackingStateMachine-prod';

exports.handler = async (event) => {
    const { orderId } = event.pathParameters;
    const { Status } = JSON.parse(event.body);
    // Validate request
    if (!orderId || !Status || Status !== 'Packed') {
        return {
            statusCode: 400,
            body: JSON.stringify({
                message: "Invalid request. Ensure orderId and status ('Packed') are provided."
            }),
        };
    }

    try {
        const getParams = {
            TableName: TableName,
            Key: { id: orderId },
        };

        const getResult = await docClient.send(new GetCommand(getParams));
        const item = getResult.Item;
        if (!item) {
            return {
                statusCode: 404,
                body: JSON.stringify({ message: "Order id not found." }),
            };
        }
        // Update the order status to "Packed"
        const updateParams = {
            TableName: TableName,
            Key: { id: orderId },
            UpdateExpression: "SET #status = :status",
            ExpressionAttributeNames: {
                "#status": "status",
            },
            ExpressionAttributeValues: {
                ":status": Status,
            },
            ReturnValues: "UPDATED_NEW"
        };
        const result = await docClient.send(new UpdateCommand(updateParams));
        // After successful DynamoDB update, trigger the Step Function
        const stepFunctionParams = {
            stateMachineArn: orderProcessSFArn,
            input: JSON.stringify({
                orderId: orderId,
                status: Status,
                timestamp: new Date().toISOString(),
                additionalDetails: item 
            })
        };
        const stepFunctionResult = await stepfunctions.startExecution(stepFunctionParams).promise();
        return {
            statusCode: 200,
            body: JSON.stringify({
                message: `Order id ${orderId} has been Packed successfully`,
                // stepFunctionExecutionArn: stepFunctionResult.executionArn
            }),
        };
    } catch (error) {
        console.error("Error processing request:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: "Internal server error",
                error: error.message
            }),
        };
    }
};
