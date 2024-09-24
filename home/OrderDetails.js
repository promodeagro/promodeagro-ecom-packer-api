const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, GetCommand } = require("@aws-sdk/lib-dynamodb");
require("dotenv").config();

const client = new DynamoDBClient({
    region: process.env.REGION || "us-east-1",
});
const docClient = DynamoDBDocumentClient.from(client);
const OrdersTableName = process.env.ORDERS_TABLE || 'Orders';
const ProductsTableName = process.env.PRODUCTS_TABLE || 'prod-promodeargo-admin-productsTable';

// Helper function to fetch product details
async function getProductDetails(productId) {
    const params = {
        TableName: ProductsTableName,
        Key: { id: productId }
    };

    try {
        const productCommand = new GetCommand(params);
        const productData = await docClient.send(productCommand);
        return productData.Item ? productData.Item.images : null; 
    } catch (error) {
        console.error(`Error fetching product ${productId}:`, error.stack || error);
        return null; 
    }
}

// Handler function for AWS Lambda
exports.handler = async (event) => {
    const orderId = event.pathParameters?.orderId;
    if (!orderId) {
        return {
            statusCode: 400,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({ message: "orderId is required" })
        };
    }

    try {
        const params = {
            TableName: OrdersTableName,
            Key: { id: orderId }
        };

        // Fetch order details
        const command = new GetCommand(params);
        const data = await docClient.send(command);

        if (!data.Item) {
            return {
                statusCode: 404,
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": true,
                },
                body: JSON.stringify({ message: "Order not found" }),
            };
        }

        // Fetch product images for each item in the order
        const itemsWithImages = await Promise.all(data.Item.items.map(async (item) => {
            const productId = item.productId;
            const images = await getProductDetails(productId); 

            return {
                Name: item.productName || "Unknown",
                Quantity: item.quantityUnits,
                unit: item.unit,
                Price: item.price,
                Images: images || []
            };
        }));

        // Construct the response based on the provided structure
        const orderDetails = {
            OrderId: data.Item.id,
            CustomerName: data.Item.customerName,
            Payment: {
                method: data.Item.paymentDetails?.method
            },
            Price: data.Item.subTotal || 0,
            items: data.Item.items.length,
            ItemsList: itemsWithImages,
            CostDetails: {
                SubTotal: data.Item.subTotal,
                ShippingCharges: data.Item.deliveryCharges,
                GrossDetails: data.Item.subTotal,
                TotalAmount: data.Item.totalPrice
            }
        };

        return {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify(orderDetails)
        };
    } catch (error) {
        console.error("Error fetching order details:", error.stack || error);
        return {
            statusCode: 500,
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": true,
            },
            body: JSON.stringify({
                message: "Error processing request",
                error: error.message || "Unknown error"
            }),
        };
    }
};
