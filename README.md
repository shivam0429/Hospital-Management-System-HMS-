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


<img width="1210" height="847" alt="image" src="https://github.com/user-attachments/assets/85ca5352-abe7-4285-8827-2431690e8440" />

<img width="1896" height="772" alt="image" src="https://github.com/user-attachments/assets/0f1a23a9-06ed-41dc-9ba1-47fe9f43b017" />

<img width="1906" height="807" alt="image" src="https://github.com/user-attachments/assets/2262e035-e951-4901-a996-96297e72a7d9" />



<img width="1900" height="690" alt="image" src="https://github.com/user-attachments/assets/329bc397-07f6-4ef8-80d7-898218100997" />
<img width="1842" height="827" alt="image" src="https://github.com/user-attachments/assets/0838a832-dee0-4974-b8b1-6dc1fa471ead" />


<img width="1917" height="802" alt="image" src="https://github.com/user-attachments/assets/ed90e4ac-27ea-43ee-9417-33da0a344798" />


<img width="1727" height="851" alt="image" src="https://github.com/user-attachments/assets/64bdfbd8-3ee3-48ff-a102-dd4d08315174" />


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
