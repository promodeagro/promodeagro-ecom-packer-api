# 🚀 PromodeAgro Ecom Packer APIs

A **Python Serverless API** for authentication, orders, notifications, and profile management, using AWS Lambda, DynamoDB, and the Serverless Framework.

---

## **Project Structure**

```
project-root/
│
├── .env                        # Environment variables (not committed)
├── requirements.txt            # Python dependencies
├── serverless.yml              # Serverless Framework config
├── README.md                   # This file
│
├── src/
│   ├── handlers/               # Lambda function handlers (auth, orders, etc.)
│   ├── commonfunctions/        # Shared utility functions
│   └── tests/                  # Automated API tests
│
├── node_modules/               # Node.js dependencies (for serverless plugins)
├── package.json                # Node.js config for serverless plugins
└── ...
```

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd promodeagro-ecom-packer-api
```

### **2. Python Virtual Environment**
```bash
python3.9 -m venv .venv
source .venv/bin/activate
```

### **3. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Install Node.js Dependencies**
```bash
npm install
```

### **5. AWS CLI Setup**
```bash
aws configure
```
- Enter your AWS Access Key, Secret Key, and region (e.g., `ap-south-1`).

### **6. Environment Variables**
Create a `.env` file in the project root:
```
USERS_TABLE=prod-promodeagro-packerTable-Users
ORDERS_TABLE=prod-promodeagro-packerTable-orders
ORDER_ITEMS_TABLE=prod-promodeagro-packerTable-orderItems
NOTIFICATION_TABLE=prod-promodeagro-packerTable-notification
AWS_REGION=ap-south-1
```

---

## **Running Locally**

### **Start Serverless Offline**
```bash
sls offline
```
- Your API will be available at: **http://localhost:3000/dev/**

---

## **API Endpoints (for Postman/curl)**

### **Auth**
- **POST** `/login` — Login
- **POST** `/forgot-password` — Forgot Password
- **POST** `/verify-otp` — Verify OTP
- **POST** `/reset-password` — Reset Password
- **POST** `/logout` — Logout

### **Orders**
- **GET** `/orders/unpacked` — List unpacked orders
- **GET** `/orders/packed` — List packed orders
- **GET** `/orders/start/{order_id}` — Get order details
- **POST** `/orders/complete` — Complete order

### **Notifications**
- **GET** `/notifications?user_id=USER_ID` — Get notifications

### **Profile**
- **GET** `/profile?user_id=USER_ID` — Get profile
- **POST** `/profile/update` — Update profile
- **POST** `/profile/change-password` — Change password

> **All endpoints are prefixed with `/dev/` when running locally.**

---

## **Testing the APIs Automatically**

### **1. Install Test Dependencies**
```bash
pip install pytest requests
```

### **2. Run the Tests**
```bash
pytest src/tests/test_api.py
```
- Results will be shown in your terminal.
- To save results:
  ```bash
  pytest src/tests/test_api.py > src/tests/results.txt
  ```

---

## **Troubleshooting**

- **502/504 or Lambda Timeout:**
  - Check your terminal for Python errors or stack traces.
  - Make sure your handler returns a valid response (`statusCode` and `body`).
  - Ensure all dependencies in `requirements.txt` are installed in your virtual environment.

- **ModuleNotFoundError:**
  - Run `pip install -r requirements.txt` in your virtual environment.

- **Environment Variables Not Loaded:**
  - Ensure `.env` is in the project root, with no leading spaces or extra characters.
  - Restart your terminal and serverless offline.

- **Unsupported Python Runtime:**
  - Use `python3.9` for local development with serverless offline.

---

## **Useful Commands**

- **Start local server:**
  ```bash
  sls offline
  ```
- **Run tests:**
  ```bash
  pytest src/tests/test_api.py
  ```
- **Deploy to AWS:**
  ```bash
  sls deploy
  ```

---

## **Contact & Contribution**
- For issues, open a GitHub issue or contact the maintainer.
- PRs are welcome!

---

**Happy Coding with Mohammed Sohail! 🚀** 