# 🏥 Hospital Management System (HMS)

A full-stack Hospital Management System built with **Python (Flask)** and **MySQL** that enables hospital administrators and patients to manage appointments, billing, and online payments through a modern web interface.

## 🌐 Live Demo

**Live Website:** https://hospital-management-system-hms-zved.onrender.com

---

# ✨ Features

## 👨‍⚕️ Admin Module

- Secure Admin Login
- Dashboard with statistics
- Manage Patients
- Manage Doctors
- Manage Departments
- Schedule Appointments
- Generate Bills
- View Payment Status
- Razorpay Payment Integration
- Dashboard Analytics

---

## 👤 Patient Module

- Patient Signup
- Secure Login
- Book Appointments
- View Personal Bills
- Online Bill Payment
- Appointment History

---

## 💳 Payment Gateway

Integrated with **Razorpay Test Mode**

- Secure Checkout
- Online Payment
- Payment Status Update
- Razorpay Order Creation
- Payment Verification

---

# 🛠 Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Backend

- Python
- Flask

### Database

- MySQL

### Payment

- Razorpay API

### Deployment

- Render
- FreeSQLDatabase

---

# 📁 Project Structure

```
hospital_management_system/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── .env.example
├── README.md
│
├── database/
│   └── schema.sql
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── patients.html
│   ├── doctors.html
│   ├── appointments.html
│   ├── bills.html
│   ├── my_bills.html
│   ├── payment.html
│   └── ...
│
└── screenshots/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/shivam0429/Hospital-Management-System-HMS-.git

cd Hospital-Management-System-HMS-
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=hospital_db

FLASK_SECRET_KEY=your_secret_key

RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

---

## Import Database

Import

```
database/schema.sql
```

into MySQL.

---

## Run Application

```bash
python app.py
```

Visit

```
http://127.0.0.1:5000
```

---

# 👤 Default Admin Login

```
Username : admin

Password : admin123
```

---

# 📸 Screenshots

Add screenshots here.

Example:

```
screenshots/
<img width="1210" height="847" alt="image" src="https://github.com/user-attachments/assets/b0a8abb3-8cd9-4578-bc60-67c7d1b0bdc7" />

<img width="1900" height="690" alt="image" src="https://github.com/user-attachments/assets/7db663f9-2c57-4f7c-8c54-feac5fa8d95e" />


<img width="1900" height="690" alt="image" src="https://github.com/user-attachments/assets/59124406-8cf1-44ae-8e67-4080016504f7" />


<img width="1917" height="802" alt="image" src="https://github.com/user-attachments/assets/0a7a1008-7b15-4ec9-822f-9ad3e1a86374" />


<img width="1727" height="851" alt="image" src="https://github.com/user-attachments/assets/63c0e6b8-d0f1-4a5b-8c54-90c607bd7772" />


---

# 🔒 Security Features

- Password Hashing
- Session Authentication
- Role Based Access
- Protected Routes
- Environment Variables
- SQL Parameterized Queries

---

# 🚀 Future Improvements

- Doctor Login Portal
- Email Notifications
- SMS Notifications
- PDF Invoice Download
- Prescription Management
- Medical Reports Upload
- Appointment Reminder
- Patient Profile
- Analytics Dashboard
- Search & Filters
- Export Reports
- REST API
- Docker Support

---

# 📦 Deployment

Hosted on

- Render
- MySQL Database
- Razorpay Test Mode

---

# 👨‍💻 Author

**Shivam Singh**

📧 Email: shivam.singh.3994@gmail.com

🔗 GitHub:
https://github.com/shivam0429

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📜 License

This project is created for educational and portfolio purposes.
