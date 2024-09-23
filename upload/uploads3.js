require("dotenv").config()
const { S3Client, PutObjectCommand } = require("@aws-sdk/client-s3")

const s3Client = new S3Client({ region: "us-east-1" })

module.exports.uploadToS3 = async ( data) => {
	const contentType = data.split(";")[0].split(":")[1]
	const fileExtension = contentType.split("/")[1]
	const bucket = process.env.BUCKET_NAME || "ecomdmsservice"
	const folder = process.env.BUCKET_FOLDER_NAME || "Product-images/"
	const buffer = Buffer.from(data.split(",")[1], "base64")
	const s3Params = {
		Bucket: bucket,
		Key: `${folder}`,
		Body: buffer,
		ContentType: contentType,
	}

	try {
		const result = await s3Client.send(new PutObjectCommand(s3Params))
		console.log(result)
		const statusCode = result.$metadata.httpStatusCode
		if (statusCode === 200) {
			console.log("sss")
			const link = `https://${bucket}.s3.amazonaws.com/${folder}`
			return { link, fileExtension, statusCode }
		}
	} catch (error) {
		console.error("Error uploading to S3:", error)
		throw error
	}
}