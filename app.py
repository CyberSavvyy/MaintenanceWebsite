from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

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

# Route to display the maintenance form
@app.route('/maintenanceForm', methods=['GET'])
def maintenance_form():
    return render_template('maintenanceRequest.html')

# Route to display the amenities form
@app.route('/amenitiesForm', methods=['GET'])
def amenities_form():
    return render_template('amenitiesForm.html')

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
