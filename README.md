# Hospital Management System - Python + SQL

A professional Hospital Management System built using **Python, Flask, MySQL, HTML, CSS**. This project is suitable for fresher Python + SQL job roles.

## Features
- Secure admin/staff login
- Dashboard with patients, doctors, appointments, and revenue stats
- Patient CRUD: add, search, update, delete
- Doctor management with departments
- Appointment booking with status update
- Billing module with generated total amount
- MySQL relational database using PK, FK, joins, constraints, and aggregate queries
- Clean responsive developer-level UI

## Tech Stack
- Python
- Flask
- MySQL
- HTML5
- CSS3

## SQL Concepts Covered
- Primary Key and Foreign Key
- Joins
- CRUD Operations
- Aggregate Functions
- Constraints
- Generated Columns
- Relational Database Design

## Setup Instructions

### 1. Create database
Open MySQL and run:
```sql
SOURCE database/schema.sql;
```
Or copy the SQL from `database/schema.sql` and execute it in MySQL Workbench.

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
Copy `.env.example` to `.env` and update your MySQL password:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=hospital_db
FLASK_SECRET_KEY=change-this-secret-key
```

### 5. Run project
```bash
python app.py
```

Open in browser:
```text
http://127.0.0.1:5000
```

Default login:
```text
Username: admin
Password: admin123
```

## Resume Description
Developed a Hospital Management System using Python, Flask, and MySQL with patient registration, doctor management, appointment booking, billing records, authentication, CRUD operations, and optimized SQL queries for efficient hospital data handling.
