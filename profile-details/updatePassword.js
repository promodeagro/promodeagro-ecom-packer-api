const AWS = require('aws-sdk');
const crypto = require('crypto');
const { z } = require('zod');
const docClient = new AWS.DynamoDB.DocumentClient();
require('dotenv').config();

exports.handler = async (event) => {
    const passwordStrengthRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/;
    
    const userUpdateSchema = z.object({
        userId: z.string().min(1, { message: "User ID is required and cannot be empty." }),
        userName: z.string().optional(),
        email: z.string().email({ message: "A valid email address is required." }).optional(),
        oldPassword: z.string().min(1, { message: "Old password is required." }),
        newPassword: z.string()
            .min(8, { message: "Password must be at least 8 characters long." })
            .regex(passwordStrengthRegex, { message: "Password must include at least one uppercase letter and one special character." }),
    });

    try {
        const parsedBody = userUpdateSchema.parse(JSON.parse(event.body));
        const { userId, userName, email, oldPassword, newPassword } = parsedBody;

        // Get user details by userId
        const userParams = {
            TableName: process.env.USERS_TABLE,
            Key: {
                UserId: userId,
            },
        };
        const data = await docClient.get(userParams).promise();
        if (!data.Item) {
            return {
                statusCode: 404,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({ message: "User not found", statusCode: 404 }),
            };
        }
        const user = data.Item;
        // Verify old password
        const oldPasswordHash = crypto.createHash('sha256').update(oldPassword).digest('hex');
        if (user.PasswordHash !== oldPasswordHash) {
            return {
                statusCode: 401,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({ message: "Old password is incorrect.", statusCode: 401 }),
            };
        }

        // Hash the new password
        const newPasswordHash = crypto.createHash('sha256').update(newPassword).digest('hex');

        // Update user password
        const updateParams = {
            TableName: process.env.USERS_TABLE,
            Key: {
                UserId: userId,
            },
            UpdateExpression: 'set PasswordHash = :newPasswordHash',
            ExpressionAttributeValues: {
                ':newPasswordHash': newPasswordHash,
            },
            ReturnValues: 'UPDATED_NEW',
        };

        await docClient.update(updateParams).promise();
        return {
            statusCode: 200,
            body: JSON.stringify({ message: "Password changed successfully.", statusCode: 200 }),
        };
    } catch (error) {
        if (error instanceof z.ZodError) {
            return {
                statusCode: 400,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({
                    message: "Validation errors occurred.",
                    errors: error.errors.map(e => `${e.path.join('.')} ${e.message}`),
                    statusCode: 400
                }),
            };
        }
        console.error("Error updating user profile:", error.stack || error);
        return {
            statusCode: 500,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({ message: "Internal Server Error", error: error.message }),
        };
    }
};
