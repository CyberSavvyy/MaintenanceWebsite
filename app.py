from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup function
def setup_database():
    connection = None
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Table creation statements
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amenities_reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            amenity TEXT NOT NULL,
            reservation_date TEXT NOT NULL,
            reservation_time TEXT NOT NULL,
            notes TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_permits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            vehicle_model TEXT NOT NULL,
            vehicle_plate TEXT NOT NULL,
            permit_type TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            contact TEXT NOT NULL,
            complaint TEXT NOT NULL
        )
        ''')

        connection.commit()
    finally:
        if connection:
            connection.close()

# Call the setup_database function before starting the app
setup_database()

# Home route
@app.route('/')
def home():
    return "Welcome to the Resident Satisfaction Dashboard!"

# Route to display the management portal
@app.route('/management', methods=['GET'])
def management_portal():
    return render_template('management.html')

# Route to fetch tickets for a specific category
@app.route('/getTickets/<category>', methods=['GET'])
def get_tickets(category):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Map category to the correct table
    table_mapping = {
        "maintenance": "maintenance_requests",
        "amenities": "amenities_reservations",
        "complaints": "complaints",
        "parking": "parking_permits"
    }

    if category not in table_mapping:
        return jsonify({"error": "Invalid category"}), 400

    table_name = table_mapping[category]
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    tickets = cursor.fetchall()
    connection.close()

    # Convert to JSON-friendly format
    tickets_list = [
        {"id": row[0], "name": row[1], "unit": row[2], "details": row[3:], "status": "Pending"}
        for row in tickets
    ]
    return jsonify(tickets_list)

# Other routes for forms
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Route to display the resident portal (index page)
@app.route('/index', methods=['GET'])
def index_page():
    return render_template('index.html')

@app.route('/maintenanceForm', methods=['GET'])
def maintenance_form():
    return render_template('maintenanceRequest.html')

@app.route('/amenitiesForm', methods=['GET'])
def amenities_form():
    return render_template('amenities.html')

@app.route('/parkingPermitsForm', methods=['GET'])
def parkingPermitsForm():
    return render_template('parkingPermits.html')

@app.route('/complaintsForm', methods=['GET'])
def complaintsForm():
    return render_template('complaints.html')

# Routes for submitting forms
@app.route('/submitMaintenance', methods=['POST'])
def submit_maintenance():
    data = request.form
    name = data['name']
    unit = data['unit']
    issue = data['issue']
    priority = data['priority']

    print(f"Received: name={name}, unit={unit}, issue={issue}, priority={priority}")  # Debugging log
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO maintenance_requests (name, unit, issue, priority)
        VALUES (?, ?, ?, ?)
    ''', (name, unit, issue, priority))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Maintenance request submitted successfully!'})

@app.route('/submitAmenities', methods=['POST'])
def submit_amenities():
    data = request.form
    name = data['name']
    unit = data['unit']
    amenity = data['amenity']
    reservation_date = data['reservation_date']
    reservation_time = data['reservation_time']
    notes = data['notes']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO amenities_reservations (name, unit, amenity, reservation_date, reservation_time, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, unit, amenity, reservation_date, reservation_time, notes))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Amenities reservation submitted successfully!'})

@app.route('/submitParkingPermit', methods=['POST'])
def submit_parking_permit():
    data = request.form
    name = data['name']
    unit = data['unit']
    vehicle_model = data['vehicle_model']
    vehicle_plate = data['vehicle_plate']
    permit_type = data['permit_type']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO parking_permits (name, unit, vehicle_model, vehicle_plate, permit_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, unit, vehicle_model, vehicle_plate, permit_type))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Parking permit request submitted successfully!'})

@app.route('/submitComplaints', methods=['POST'])
def submit_complaint():
    data = request.form
    name = data['name']
    unit = data['unit']
    contact = data['contact']
    complaint = data['complaint']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO complaints (name, unit, contact, complaint)
        VALUES (?, ?, ?, ?)
    ''', (name, unit, contact, complaint))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Complaint submitted successfully!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
