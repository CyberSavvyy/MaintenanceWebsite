from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup function (already in your code)
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
            date TEXT NOT NULL,
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
            reservation_time TEXT NOT NULL
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

# Route for submitting maintenance requests
@app.route('/submitMaintenance', methods=['POST'])
def submit_maintenance():
    data = request.form
    name = data['name']
    unit = data['unit']
    issue = data['issue']
    date = data['date']
    priority = data['priority']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO maintenance_requests (name, unit, issue, date, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, unit, issue, date, priority))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Maintenance request submitted successfully!'})

# Route for submitting amenities reservations
@app.route('/submitAmenities', methods=['POST'])
def submit_amenities():
    data = request.form
    name = data['name']
    unit = data['unit']
    amenity = data['amenity']
    reservation_date = data['reservation_date']
    reservation_time = data['reservation_time']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO amenities_reservations (name, unit, amenity, reservation_date, reservation_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, unit, amenity, reservation_date, reservation_time))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Amenities reservation submitted successfully!'})

# Route for submitting complaints
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
