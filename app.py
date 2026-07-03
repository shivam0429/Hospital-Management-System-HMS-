import os
import hashlib
from functools import wraps

import razorpay
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session

load_dotenv()
load_dotenv(".env.payment")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "hospital-dev-secret")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "hospital_db")
}

razorpay_client = razorpay.Client(auth=(
    os.getenv("RAZORPAY_KEY_ID"),
    os.getenv("RAZORPAY_KEY_SECRET")
))


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(query, params=None):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params or ())
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def fetch_one(query, params=None):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params or ())
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data


def execute(query, params=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    cur.close()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


@app.route("/patient-signup", methods=["GET", "POST"])
def patient_signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = hash_password(request.form["password"])
        age = request.form["age"]
        gender = request.form["gender"]
        address = request.form["address"]

        existing = fetch_one("SELECT * FROM users WHERE username=%s", (email,))
        if existing:
            flash("Email already registered. Please login.", "danger")
            return redirect(url_for("patient_signup"))

        execute("""
            INSERT INTO users(username, password_hash, role)
            VALUES(%s,%s,%s)
        """, (email, password, "Patient"))

        user = fetch_one("SELECT id FROM users WHERE username=%s", (email,))

        execute("""
            INSERT INTO patients(user_id, name, age, gender, phone, address, blood_group, medical_history)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """, (user["id"], name, age, gender, phone, address, "N/A", "Not provided"))

        flash("Signup successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("patient_signup.html")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = hash_password(request.form["password"])

        user = fetch_one(
            "SELECT * FROM users WHERE username=%s AND password_hash=%s",
            (username, password)
        )

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            flash("Login successful.", "success")

            if user["role"] == "Patient":
                return redirect(url_for("book_appointment"))

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    if session.get("role") == "Patient":
        return redirect(url_for("book_appointment"))

    stats = {
        "patients": fetch_one("SELECT COUNT(*) AS total FROM patients")["total"],
        "doctors": fetch_one("SELECT COUNT(*) AS total FROM doctors")["total"],
        "appointments": fetch_one(
            "SELECT COUNT(*) AS total FROM appointments WHERE status='Scheduled'"
        )["total"],
        "revenue": fetch_one(
            "SELECT COALESCE(SUM(total_amount),0) AS total FROM bills WHERE payment_status='Paid'"
        )["total"],
    }

    upcoming = fetch_all("""
        SELECT a.id, a.appointment_date, a.appointment_time, a.status,
               p.name AS patient_name, d.name AS doctor_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
        LIMIT 6
    """)

    return render_template("dashboard.html", stats=stats, upcoming=upcoming)


@app.route("/patients")
@login_required
def patients():
    q = request.args.get("q", "").strip()

    if q:
        data = fetch_all("""
            SELECT * FROM patients
            WHERE name LIKE %s OR phone LIKE %s OR blood_group LIKE %s
            ORDER BY id DESC
        """, (f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        data = fetch_all("SELECT * FROM patients ORDER BY id DESC")

    return render_template("patients.html", patients=data, q=q)


@app.route("/patients/add", methods=["GET", "POST"])
@login_required
def add_patient():
    if request.method == "POST":
        execute("""
            INSERT INTO patients(name, age, gender, phone, address, blood_group, medical_history)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["name"],
            request.form["age"],
            request.form["gender"],
            request.form["phone"],
            request.form["address"],
            request.form["blood_group"],
            request.form["medical_history"]
        ))

        flash("Patient added successfully.", "success")
        return redirect(url_for("patients"))

    return render_template("patient_form.html", patient=None)


@app.route("/patients/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_patient(id):
    patient = fetch_one("SELECT * FROM patients WHERE id=%s", (id,))

    if request.method == "POST":
        execute("""
            UPDATE patients
            SET name=%s, age=%s, gender=%s, phone=%s, address=%s,
                blood_group=%s, medical_history=%s
            WHERE id=%s
        """, (
            request.form["name"],
            request.form["age"],
            request.form["gender"],
            request.form["phone"],
            request.form["address"],
            request.form["blood_group"],
            request.form["medical_history"],
            id
        ))

        flash("Patient updated successfully.", "success")
        return redirect(url_for("patients"))

    return render_template("patient_form.html", patient=patient)


@app.route("/patients/delete/<int:id>")
@login_required
def delete_patient(id):
    execute("DELETE FROM patients WHERE id=%s", (id,))
    flash("Patient deleted successfully.", "info")
    return redirect(url_for("patients"))


@app.route("/doctors", methods=["GET", "POST"])
@login_required
def doctors():
    departments = fetch_all("SELECT * FROM departments ORDER BY name")

    if request.method == "POST":
        execute("""
            INSERT INTO doctors(name, specialization, phone, email, department_id, availability)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (
            request.form["name"],
            request.form["specialization"],
            request.form["phone"],
            request.form["email"],
            request.form["department_id"],
            request.form["availability"]
        ))

        flash("Doctor added successfully.", "success")
        return redirect(url_for("doctors"))

    data = fetch_all("""
        SELECT d.*, dep.name AS department
        FROM doctors d
        LEFT JOIN departments dep ON d.department_id = dep.id
        ORDER BY d.id DESC
    """)

    return render_template("doctors.html", doctors=data, departments=departments)


@app.route("/doctors/delete/<int:id>")
@login_required
def delete_doctor(id):
    execute("DELETE FROM doctors WHERE id=%s", (id,))
    flash("Doctor deleted successfully.", "info")
    return redirect(url_for("doctors"))


@app.route("/appointments", methods=["GET", "POST"])
@login_required
def appointments():
    patients_data = fetch_all("SELECT id, name FROM patients ORDER BY name")
    doctors_data = fetch_all("SELECT id, name, specialization FROM doctors ORDER BY name")

    if request.method == "POST":
        execute("""
            INSERT INTO appointments(patient_id, doctor_id, appointment_date, appointment_time, status, notes)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (
            request.form["patient_id"],
            request.form["doctor_id"],
            request.form["appointment_date"],
            request.form["appointment_time"],
            request.form["status"],
            request.form["notes"]
        ))

        flash("Appointment saved successfully.", "success")
        return redirect(url_for("appointments"))

    data = fetch_all("""
        SELECT a.*, p.name AS patient_name, d.name AS doctor_name, d.specialization
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
    """)

    return render_template(
        "appointments.html",
        appointments=data,
        patients=patients_data,
        doctors=doctors_data
    )


@app.route("/appointments/status/<int:id>/<status>")
@login_required
def appointment_status(id, status):
    if status in ["Scheduled", "Completed", "Cancelled"]:
        execute("UPDATE appointments SET status=%s WHERE id=%s", (status, id))
        flash("Appointment status updated.", "success")

    return redirect(url_for("appointments"))


@app.route("/bills", methods=["GET", "POST"])
@login_required
def bills():
    if session.get("role") == "Patient":
        return redirect(url_for("my_bills"))

    patients_data = fetch_all("SELECT id, name FROM patients ORDER BY name")

    appointments_data = fetch_all("""
        SELECT a.id, p.name patient_name, d.name doctor_name, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.id DESC
    """)

    if request.method == "POST":
        appointment_id = request.form.get("appointment_id") or None

        consultation_fee = float(request.form["consultation_fee"])
        medicine_fee = float(request.form["medicine_fee"])
        lab_fee = float(request.form["lab_fee"])
        total_amount = consultation_fee + medicine_fee + lab_fee

        execute("""
            INSERT INTO bills(
                patient_id, appointment_id, consultation_fee,
                medicine_fee, lab_fee, total_amount, payment_status
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (
            request.form["patient_id"],
            appointment_id,
            consultation_fee,
            medicine_fee,
            lab_fee,
            total_amount,
            request.form["payment_status"]
        ))

        flash("Bill generated successfully.", "success")
        return redirect(url_for("bills"))

    data = fetch_all("""
        SELECT b.*, p.name AS patient_name
        FROM bills b
        JOIN patients p ON b.patient_id = p.id
        ORDER BY b.id DESC
    """)

    return render_template(
        "bills.html",
        bills=data,
        patients=patients_data,
        appointments=appointments_data
    )


@app.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    if session.get("role") != "Patient":
        flash("Only patients can access this page.", "danger")
        return redirect(url_for("dashboard"))

    doctors_data = fetch_all("""
        SELECT id, name, specialization, consultation_fee
        FROM doctors
        ORDER BY name
    """)

    if request.method == "POST":
        doctor_id = request.form["doctor_id"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]

        patient = fetch_one(
            "SELECT id FROM patients WHERE user_id=%s",
            (session["user_id"],)
        )

        if not patient:
            flash("Patient profile not found. Please sign up again.", "danger")
            return redirect(url_for("patient_signup"))

        doctor = fetch_one(
            "SELECT consultation_fee FROM doctors WHERE id=%s",
            (doctor_id,)
        )

        fee = float(doctor["consultation_fee"])

        execute("""
            INSERT INTO appointments(patient_id, doctor_id, appointment_date, appointment_time, status, notes)
            VALUES(%s,%s,%s,%s,%s,%s)
        """, (
            patient["id"],
            doctor_id,
            appointment_date,
            appointment_time,
            "Scheduled",
            "Booked by patient"
        ))

        appointment = fetch_one("SELECT id FROM appointments ORDER BY id DESC LIMIT 1")

        execute("""
            INSERT INTO bills(
                patient_id, appointment_id, consultation_fee,
                medicine_fee, lab_fee, total_amount, payment_status
            )
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (
            patient["id"],
            appointment["id"],
            fee,
            0,
            0,
            fee,
            "Pending"
        ))

        flash("Appointment booked successfully. Please pay your consultation fee.", "success")
        return redirect(url_for("my_bills"))

    return render_template("book_appointment.html", doctors=doctors_data)


@app.route("/my-bills")
@login_required
def my_bills():
    if session.get("role") != "Patient":
        flash("Only patients can access this page.", "danger")
        return redirect(url_for("dashboard"))

    bills_data = fetch_all("""
        SELECT b.*, p.name AS patient_name
        FROM bills b
        JOIN patients p ON b.patient_id = p.id
        WHERE p.user_id=%s
        ORDER BY b.id DESC
    """, (session["user_id"],))

    return render_template("my_bills.html", bills=bills_data)


@app.route("/pay/<int:bill_id>")
@login_required
def pay_bill(bill_id):
    bill = fetch_one("SELECT * FROM bills WHERE id=%s", (bill_id,))

    if not bill:
        flash("Bill not found.", "danger")
        return redirect(url_for("my_bills" if session.get("role") == "Patient" else "bills"))

    if session.get("role") == "Patient":
        patient = fetch_one(
            "SELECT id FROM patients WHERE user_id=%s",
            (session["user_id"],)
        )

        if not patient or bill["patient_id"] != patient["id"]:
            flash("You are not allowed to pay this bill.", "danger")
            return redirect(url_for("my_bills"))

    amount = int(float(bill["total_amount"]) * 100)

    if amount < 100:
        flash("Bill amount must be at least ₹1 for online payment.", "danger")
        return redirect(url_for("my_bills" if session.get("role") == "Patient" else "bills"))

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    execute(
        "UPDATE bills SET order_id=%s WHERE id=%s",
        (order["id"], bill_id)
    )

    return render_template(
        "payment.html",
        bill=bill,
        order_id=order["id"],
        key=os.getenv("RAZORPAY_KEY_ID"),
        amount=amount
    )


@app.route("/payment-success/<int:bill_id>")
@login_required
def payment_success(bill_id):
    payment_id = request.args.get("payment_id")
    order_id = request.args.get("order_id")
    signature = request.args.get("signature")

    execute("""
        UPDATE bills
        SET payment_status='Paid',
            payment_id=%s,
            order_id=%s,
            payment_signature=%s
        WHERE id=%s
    """, (payment_id, order_id, signature, bill_id))

    flash("Payment successful.", "success")

    if session.get("role") == "Patient":
        return redirect(url_for("my_bills"))

    return redirect(url_for("bills"))


@app.errorhandler(Error)
def db_error(error):
    return f"Database error: {error}. Please check MySQL connection and run database/schema.sql", 500


if __name__ == "__main__":
    app.run(debug=True)run(debug=True)
