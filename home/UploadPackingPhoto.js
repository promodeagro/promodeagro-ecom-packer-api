const { z } = require("zod");
const { uploadToS3 } = require("../upload/uploads3");
const AWS = require("aws-sdk");

const dynamoDB = new AWS.DynamoDB.DocumentClient();
const TableName = process.env.PACKEDITEMS || 'PackedItems'; 

exports.handler = async event => {
    const orderId = event.pathParameters?.orderId;
    const orderIdSchema = z.string().regex(/^\d{3}-\d{7}-\d{7}$/); 
    const isOrderIdValid = orderIdSchema.safeParse(orderId);
    if (!isOrderIdValid.success) {
        return {
            statusCode: 400,
            headers: {
                "Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({
                error: isOrderIdValid.error.issues[0].message,
            }),
        };
    }
    const { data } = JSON.parse(event.body);

    // Validate inputs
    const metadocsObj = {
        data: data,
    };
    const metadocsSchema = z.object({
        data: z.string({
            message: "invalid string",
        }),
    });
    const result = metadocsSchema.safeParse(metadocsObj);
    if (!result.success) {
        return {
            statusCode: 400,
            headers: {
                "Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({
                error: result.error.formErrors.fieldErrors,
            }),
        };
    }
    const currentTimestamp = new Date().toISOString();
    try {
        // Check if the data is a URL
        const isLink = isURL(data);
        if (isLink) {
            // Store URL and other details directly in DynamoDB
            const dynamoParams = {
                TableName: TableName,
                Item: {
                    OrderId: orderId,
                    photoUrl: data,      
                    createdAt: currentTimestamp, 
                    type: "url"
                },
            };

            await dynamoDB.put(dynamoParams).promise();

            return {
                statusCode: 200,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({
                    message: "Photo uploaded successfully",
                    photoUrl: data
                }),
            };
        }

        // Upload to S3 if data is not a URL
        const upload = await uploadToS3( data);
        console.log("upload:", upload.link);
        const url = upload.link;
        const type = upload.fileExtension;
        const statusCode = upload.statusCode;

        // If upload is successful
        if (statusCode === 200) {
            const uuid = crypto.randomUUID();
        // Store in DynamoDB
            const dynamoParams = {
                TableName: TableName,
                Item: {
                    id:uuid,
                    OrderId: orderId,
                    photoUrl: url,
                    createdAt: currentTimestamp, 
                },
            };

            await dynamoDB.put(dynamoParams).promise();

            return {
                statusCode: 200,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({
                    photoUrl: url,
                    // type: type,
                    OrderId:orderId
                }),
            };
        }
    } catch (error) {
        console.error("Error inserting data:", error);
        return {
            statusCode: 500,
            headers: {
                "Access-Control-Allow-Origin": "*",
				"Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({
                message: error.message,
                error: error,
            }),
        };
    }
};

// Helper function to validate URL format
function isURL(str) {
    const urlRegex = /^(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+$/;
    return urlRegex.test(str);
}
