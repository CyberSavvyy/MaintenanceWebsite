from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Database setup function
def setup_database():
    connection = None
    try:
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Table creation with fixed commas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'open'
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
            notes TEXT NOT NULL,
            status TEXT DEFAULT 'open'
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_permits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            vehicle_model TEXT NOT NULL,
            vehicle_plate TEXT NOT NULL,
            permit_type TEXT NOT NULL,
            status TEXT DEFAULT 'open'
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            contact TEXT NOT NULL,
            complaint TEXT NOT NULL,
            status TEXT DEFAULT 'open'
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
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Fetch tickets from all tables
    cursor.execute('SELECT * FROM maintenance_requests')
    maintenance_tickets = [
        {"id": row[0], "name": row[1], "unit": row[2], "details": row[3], "priority": row[4], "status": row[5], "category": "maintenance_requests"}
        for row in cursor.fetchall()
    ]

    cursor.execute('SELECT * FROM amenities_reservations')
    amenities_tickets = [
        {"id": row[0], "name": row[1], "unit": row[2], "details": row[3], "priority": "N/A", "status": row[7], "category": "amenities_reservations"}
        for row in cursor.fetchall()
    ]

    cursor.execute('SELECT * FROM parking_permits')
    parking_tickets = [
        {"id": row[0], "name": row[1], "unit": row[2], "details": f"Vehicle: {row[3]}, Plate: {row[4]}, Type: {row[5]}", "priority": "N/A", "status": row[6], "category": "parking_permits"}
        for row in cursor.fetchall()
    ]

    cursor.execute('SELECT * FROM complaints')
    complaints_tickets = [
        {"id": row[0], "name": row[1], "unit": row[2], "details": row[4], "priority": "N/A", "status": row[5], "category": "complaints"}
        for row in cursor.fetchall()
    ]

    connection.close()

    # Combine all tickets
    all_tickets = maintenance_tickets + amenities_tickets + parking_tickets + complaints_tickets

    # Render the management page with tickets
    return render_template('management.html', tickets=all_tickets)

# Route to mark tickets as resolved
@app.route('/resolveTicket', methods=['POST'])
def resolve_ticket():
    data = request.json
    ticket_id = data.get('id')
    category = data.get('category')

    # Map category to table name
    table_mapping = {
        "maintenance": "maintenance_requests",
        "amenities": "amenities_reservations",
        "complaints": "complaints",
        "parking": "parking_permits"
    }

    if category not in table_mapping:
        return jsonify({"error": "Invalid category"}), 400

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Update the status to 'resolved'
    table_name = table_mapping[category]
    cursor.execute(f'''
        UPDATE {table_name}
        SET status = 'resolved'
        WHERE id = ?
    ''', (ticket_id,))
    connection.commit()
    connection.close()

    return jsonify({"message": "Ticket marked as resolved!"})

# Other routes for forms
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
