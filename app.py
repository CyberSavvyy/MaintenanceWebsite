from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

# Initialize Flask app and enable CORS for cross-origin resource sharing
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup function
def setup_database():
    connection = None
    try:
        # Connect to SQLite database (or create it if it doesn't exist)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Create table for maintenance requests if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL
        )
        ''')

        # Create table for amenities reservations
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

        # Create table for parking permits
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

        # Create table for complaints
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            unit TEXT NOT NULL,
            contact TEXT NOT NULL,
            complaint TEXT NOT NULL
        )
        ''')

        # Commit the changes to the database
        connection.commit()
    finally:
        if connection:
            # Close the database connection to release resources
            connection.close()

# Call the database setup function before starting the app
setup_database()

# Define a route for the home page
@app.route('/')
def home():
    return "Welcome to the Resident Satisfaction Dashboard!"

# Define a route to render the management portal
@app.route('/management', methods=['GET'])
def management_portal():
    return render_template('management.html')

# Define a route to fetch tickets for a specific category
@app.route('/getTickets/<category>', methods=['GET'])
def get_tickets(category):
    connection = sqlite3.connect('database.db')  # Connect to the database
    cursor = connection.cursor()

    # Map category names to their respective database tables
    table_mapping = {
        "maintenance": "maintenance_requests",
        "amenities": "amenities_reservations",
        "complaints": "complaints",
        "parking": "parking_permits"
    }

    # Handle invalid category requests
    if category not in table_mapping:
        return jsonify({"error": "Invalid category"}), 400

    # Query the database for the specified category
    table_name = table_mapping[category]
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    tickets = cursor.fetchall()  # Fetch all matching rows
    connection.close()  # Close the connection

    # Format the fetched tickets into a JSON-friendly format
    tickets_list = [
        {"id": row[0], "name": row[1], "unit": row[2], "details": row[3:], "status": "Pending"}
        for row in tickets
    ]
    return jsonify(tickets_list)

# Define a route to render the login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Define a route to render the resident portal (index page)
@app.route('/index', methods=['GET'])
def index_page():
    return render_template('index.html')

# Define routes to render forms for different categories
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Simple authentication logic (placeholder for a real authentication system)
        if email == 'admin@example.com' and password == 'password':
            # Redirect to the resident portal (index page) on successful login
            return render_template('index.html')
        else:
            # Return an error message for invalid credentials
            return "Invalid credentials, please try again!", 401

    # Render the login page for GET requests
    return render_template('login.html')

# Route to handle submission of maintenance requests
@app.route('/submitMaintenance', methods=['POST'])
def submit_maintenance():
    # Extract form data
    data = request.form
    name = data['name']
    unit = data['unit']
    issue = data['issue']
    priority = data['priority']

    # Debugging log to verify received data
    print(f"Received: name={name}, unit={unit}, issue={issue}, priority={priority}")

    # Insert the data into the maintenance_requests table
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO maintenance_requests (name, unit, issue, priority)
        VALUES (?, ?, ?, ?)
    ''', (name, unit, issue, priority))
    connection.commit()
    connection.close()

    # Return a success message as JSON
    return jsonify({'message': 'Maintenance request submitted successfully!'})

# Route to handle submission of amenities reservations
@app.route('/submitAmenities', methods=['POST'])
def submit_amenities():
    # Extract form data
    data = request.form
    name = data['name']
    unit = data['unit']
    amenity = data['amenity']
    reservation_date = data['reservation_date']
    reservation_time = data['reservation_time']
    notes = data['notes']

    # Insert the data into the amenities_reservations table
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO amenities_reservations (name, unit, amenity, reservation_date, reservation_time, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, unit, amenity, reservation_date, reservation_time, notes))
    connection.commit()
    connection.close()

    # Return a success message as JSON
    return jsonify({'message': 'Amenities reservation submitted successfully!'})

# Route to handle submission of parking permits
@app.route('/submitParkingPermit', methods=['POST'])
def submit_parking_permit():
    # Extract form data
    data = request.form
    name = data['name']
    unit = data['unit']
    vehicle_model = data['vehicle_model']
    vehicle_plate = data['vehicle_plate']
    permit_type = data['permit_type']

    # Insert the data into the parking_permits table
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO parking_permits (name, unit, vehicle_model, vehicle_plate, permit_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, unit, vehicle_model, vehicle_plate, permit_type))
    connection.commit()
    connection.close()

    # Return a success message as JSON
    return jsonify({'message': 'Parking permit request submitted successfully!'})

# Route to handle submission of complaints
@app.route('/submitComplaints', methods=['POST'])
def submit_complaint():
    # Extract form data
    data = request.form
    name = data['name']
    unit = data['unit']
    contact = data['contact']
    complaint = data['complaint']

    # Insert the data into the complaints table
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO complaints (name, unit, contact, complaint)
        VALUES (?, ?, ?, ?)
    ''', (name, unit, contact, complaint))
    connection.commit()
    connection.close()

    # Return a success message as JSON
    return jsonify({'message': 'Complaint submitted successfully!'})

# Main block to run the Flask app
if __name__ == '__main__':
    # Run the app in debug mode, accessible from all network interfaces
    app.run(debug=True, host='0.0.0.0')
