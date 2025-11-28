# 🛍️ Django + Stripe Payment App

🧠 Overview

This project is a mini full-stack Django + PostgreSQL + Stripe (test-mode) web app that simulates a tiny online store.
It displays 3 fixed products, allows users to select quantities, make test payments via Stripe Checkout, and see their paid orders instantly on the same page.

💡 It’s designed to demonstrate backend–frontend integration, payment processing, and state consistency in a clean, production-style setup.

---
## 🧩 Key Features


✨ 3 predefined products displayed on the homepage
- 🛒 Quantity input + Buy Now button
- 💳 Stripe Checkout integration (test mode)
- 🔄 Robust prevention of double payments / refresh errors
- 📃 “My Orders” list after successful payment
- 🎨 Optional Bootstrap-based UI


## ⚙️ Tech Stack
| 🔧 Category          | 🧰 Tool / Library               | 💬 Purpose              |
| -------------------- | ------------------------------- | ----------------------- |
| Backend              | **Django**                      | Web framework           |
| Database             | **PostgreSQL**                  | Product & order storage |
| Payment              | **Stripe (Test Mode)**          | Secure checkout         |
| Frontend             | **HTML / CSS / Bootstrap**      | Interface & styling     |
| Config               | **python-dotenv**               | Environment variables   |
| Libraries            | **stripe**, **psycopg2-binary** | Stripe API, DB driver   |
| Container (optional) | **Docker**                      | Environment setup       |
| Tools                | **VS Code / Cursor / ChatGPT**  | Dev & AI assist         |


## 💡 Assumptions

- No user authentication (single-user demo).

- Products are static/fixed (seeded once).

- Using Stripe Checkout (simpler & secure).

- App runs in Stripe test mode only.


## 🔄 Flow Chosen: Stripe Checkout

✅ Why Checkout?

Handles payments securely on Stripe’s side.

Simplifies PCI compliance.

Redirects automatically to success/cancel URLs.

Great for small-scale e-commerce prototypes.

# 🧱 Database Models

🧾 Product
| Field       | Type         | Description    |
| ----------- | ------------ | -------------- |
| name        | CharField    | Product name   |
| price_cents | IntegerField | Price in cents |

💰 Order
| Field                 | Type                | Description         |
| --------------------- | ------------------- | ------------------- |
| product               | ForeignKey(Product) | Purchased product   |
| quantity              | IntegerField        | Units bought        |
| amount_cents          | IntegerField        | Total (price × qty) |
| paid                  | BooleanField        | Payment status      |
| stripe_payment_intent | CharField           | Stripe session ID   |
| created_at            | DateTimeField       | Timestamp           |


## 🔐 How We Prevent Double Payments

🧠 Our protection strategy:

- Create an Order with paid=False before redirecting to Stripe.

- Store each order’s unique Stripe session ID.

- After redirect back, verify session & mark as paid.

- Use POST → Redirect → GET pattern to avoid re-submits.

## ⚙️ Setup Instructions

Follow these steps to get the app running locally 👇

1. **Create Virtual Environment:**
   ```bash
   python -m venv venv

2. **Activate it**:
 windows:
  ```bash
  venv\Scripts\activate

3. **Create Virtual Environment**:
  macOs/Linux:
   ```bash
   python -m venv venv



   

 
 
 
 
 macOS/Linux:
 ```bash
source venv/bin/activate
2️⃣ Install Requirements

pip install -r requirements.txt
3️⃣ Create .env File

Copy example → real .env:
cp .env.example .env
Then add your Stripe test keys:
STRIPE_PUBLIC_KEY=pk_test_************
STRIPE_SECRET_KEY=sk_test_************
DEBUG=True

4️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
(Optional) Add sample products:
python manage.py shell
from shop.models import Product
Product.objects.create(name="Product A", price_cents=1000)
Product.objects.create(name="Product B", price_cents=1500)
Product.objects.create(name="Product C", price_cents=2000)
exit()
