from flask import Flask, request, jsonify
import mysql.connector
import json
from datetime import datetime, date
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

# Helper function to convert datetime/date objects to string for JSON serialization
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# Custom JSON encoder for MySQL results
def convert_to_json(data, cursor):
    result = []
    columns = [column[0] for column in cursor.description]
    for row in data:
        result.append(dict(zip(columns, row)))
    return result

# API Routes
@app.route('/')
def index():
    return jsonify({"message": "Disaster Relief Management API", "status": "online"})

# Relief Camp Routes
@app.route('/api/relief_camps', methods=['GET'])
def get_relief_camps():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM ReliefCamp")
        camps = cursor.fetchall()
        result = convert_to_json(camps, cursor)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/relief_camps/<int:camp_id>', methods=['GET'])
def get_relief_camp(camp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM ReliefCamp WHERE camp_id = %s", (camp_id,))
        camp = cursor.fetchone()
        
        if not camp:
            return jsonify({"success": False, "message": "Camp not found"}), 404
            
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, camp))
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/relief_camps', methods=['POST'])
def add_relief_camp():
    data = request.json
    
    # Validate required fields
    required_fields = ['camp_name', 'location', 'capacity', 'contact_person']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get max camp_id and increment by 1 for new record
        cursor.execute("SELECT MAX(camp_id) FROM ReliefCamp")
        max_id = cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1
        
        cursor.execute(
            "INSERT INTO ReliefCamp (camp_id, camp_name, location, capacity, contact_person) VALUES (%s, %s, %s, %s, %s)",
            (new_id, data['camp_name'], data['location'], data['capacity'], data['contact_person'])
        )
        conn.commit()
        
        return jsonify({"success": True, "message": "Relief camp added successfully", "camp_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/relief_camps/<int:camp_id>', methods=['PUT'])
def update_relief_camp(camp_id):
    data = request.json
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if camp exists
        cursor.execute("SELECT * FROM ReliefCamp WHERE camp_id = %s", (camp_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Camp not found"}), 404
        
        # Update the camp
        update_fields = []
        update_values = []
        
        if 'camp_name' in data:
            update_fields.append("camp_name = %s")
            update_values.append(data['camp_name'])
            
        if 'location' in data:
            update_fields.append("location = %s")
            update_values.append(data['location'])
            
        if 'capacity' in data:
            update_fields.append("capacity = %s")
            update_values.append(data['capacity'])
            
        if 'contact_person' in data:
            update_fields.append("contact_person = %s")
            update_values.append(data['contact_person'])
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
            
        query = f"UPDATE ReliefCamp SET {', '.join(update_fields)} WHERE camp_id = %s"
        update_values.append(camp_id)
        
        cursor.execute(query, tuple(update_values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Relief camp updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/relief_camps/<int:camp_id>', methods=['DELETE'])
def delete_relief_camp(camp_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if camp exists
        cursor.execute("SELECT * FROM ReliefCamp WHERE camp_id = %s", (camp_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Camp not found"}), 404
        
        # Check for related records in other tables
        cursor.execute("SELECT COUNT(*) FROM VictimSurvivor WHERE camp_id = %s", (camp_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete camp with associated victims"}), 400
            
        cursor.execute("SELECT COUNT(*) FROM Inventory WHERE camp_id = %s", (camp_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete camp with associated inventory items"}), 400
            
        cursor.execute("SELECT COUNT(*) FROM VolunteerAssignment WHERE camp_id = %s", (camp_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete camp with assigned volunteers"}), 400
            
        cursor.execute("SELECT COUNT(*) FROM MissingPersonReport WHERE camp_id = %s", (camp_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete camp with associated missing person reports"}), 400
        
        # Delete the camp
        cursor.execute("DELETE FROM ReliefCamp WHERE camp_id = %s", (camp_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Relief camp deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Victim Management Routes
@app.route('/api/victims', methods=['GET'])
def get_victims():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT v.*, c.camp_name 
            FROM VictimSurvivor v 
            LEFT JOIN ReliefCamp c ON v.camp_id = c.camp_id
        """)
        victims = cursor.fetchall()
        result = convert_to_json(victims, cursor)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/victims/<int:victim_id>', methods=['GET'])
def get_victim(victim_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT v.*, c.camp_name 
            FROM VictimSurvivor v 
            LEFT JOIN ReliefCamp c ON v.camp_id = c.camp_id
            WHERE v.victim_id = %s
        """, (victim_id,))
        victim = cursor.fetchone()
        
        if not victim:
            return jsonify({"success": False, "message": "Victim not found"}), 404
            
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, victim))
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/victims', methods=['POST'])
def add_victim():
    data = request.json if request.is_json else request.form.to_dict()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get max victim_id and increment by 1 for new record
        cursor.execute("SELECT MAX(victim_id) FROM VictimSurvivor")
        max_id = cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1
        
        # Build query based on available data
        fields = ['victim_id', 'first_name', 'last_name']
        values = [new_id, data['first_name'], data['last_name']]
        
        # Optional fields
        if 'date_of_birth' in data and data['date_of_birth']:
            fields.append('date_of_birth')
            values.append(data['date_of_birth'])
            
        if 'contact_no' in data and data['contact_no']:
            fields.append('contact_no')
            values.append(data['contact_no'])
            
        if 'address' in data and data['address']:
            fields.append('address')
            values.append(data['address'])
            
        if 'camp_id' in data and data['camp_id']:
            fields.append('camp_id')
            values.append(data['camp_id'])
        
        # Create placeholders for SQL query
        placeholders = ', '.join(['%s'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO VictimSurvivor ({field_names}) VALUES ({placeholders})"
        cursor.execute(query, tuple(values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Victim added successfully", "victim_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/victims/<int:victim_id>', methods=['PUT'])
def update_victim(victim_id):
    data = request.json if request.is_json else request.form.to_dict()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if victim exists
        cursor.execute("SELECT * FROM VictimSurvivor WHERE victim_id = %s", (victim_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Victim not found"}), 404
        
        # Update the victim details
        update_fields = []
        update_values = []
        
        if 'first_name' in data and data['first_name']:
            update_fields.append("first_name = %s")
            update_values.append(data['first_name'])
            
        if 'last_name' in data and data['last_name']:
            update_fields.append("last_name = %s")
            update_values.append(data['last_name'])
            
        if 'date_of_birth' in data:
            update_fields.append("date_of_birth = %s")
            update_values.append(data['date_of_birth'] if data['date_of_birth'] else None)
            
        if 'contact_no' in data:
            update_fields.append("contact_no = %s")
            update_values.append(data['contact_no'] if data['contact_no'] else None)
            
        if 'address' in data:
            update_fields.append("address = %s")
            update_values.append(data['address'] if data['address'] else None)
            
        if 'camp_id' in data:
            update_fields.append("camp_id = %s")
            update_values.append(data['camp_id'] if data['camp_id'] else None)
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
            
        query = f"UPDATE VictimSurvivor SET {', '.join(update_fields)} WHERE victim_id = %s"
        update_values.append(victim_id)
        
        cursor.execute(query, tuple(update_values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Victim updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/victims/<int:victim_id>', methods=['DELETE'])
def delete_victim(victim_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if victim exists
        cursor.execute("SELECT * FROM VictimSurvivor WHERE victim_id = %s", (victim_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Victim not found"}), 404
        
        # Check for related records in other tables
        cursor.execute("SELECT COUNT(*) FROM MissingPersonReport WHERE victim_id = %s", (victim_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete victim with associated missing person reports"}), 400
        
        # Delete the victim
        cursor.execute("DELETE FROM VictimSurvivor WHERE victim_id = %s", (victim_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Victim deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Missing Person Report Routes
@app.route('/api/missing_persons', methods=['GET'])
def get_missing_persons():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT m.*, c.camp_name 
            FROM MissingPersonReport m 
            LEFT JOIN ReliefCamp c ON m.camp_id = c.camp_id
        """)
        reports = cursor.fetchall()
        result = convert_to_json(reports, cursor)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/missing_persons/<int:report_id>', methods=['GET'])
def get_missing_person(report_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT m.*, c.camp_name 
            FROM MissingPersonReport m 
            LEFT JOIN ReliefCamp c ON m.camp_id = c.camp_id
            WHERE m.report_id = %s
        """, (report_id,))
        report = cursor.fetchone()
        
        if not report:
            return jsonify({"success": False, "message": "Missing person report not found"}), 404
            
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, report))
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/missing_persons', methods=['POST'])
def add_missing_person():
    data = request.json if request.is_json else request.form.to_dict()
    
    # Validate required fields
    required_fields = ['reporter_name', 'missing_person_name', 'last_seen_location', 'contact']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get max report_id and increment by 1 for new record
        cursor.execute("SELECT MAX(report_id) FROM MissingPersonReport")
        max_id = cursor.fetchone()[0]
        new_id = 1 if max_id is None else max_id + 1
        
        # Get current date if not provided
        date_reported = data.get('date_reported', date.today().isoformat())
        
        # Build query based on available data
        fields = ['report_id', 'reporter_name', 'missing_person_name', 'last_seen_location', 'date_reported', 'contact']
        values = [new_id, data['reporter_name'], data['missing_person_name'], data['last_seen_location'], date_reported, data['contact']]
        
        # Optional fields
        if 'camp_id' in data and data['camp_id']:
            fields.append('camp_id')
            values.append(data['camp_id'])
            
        if 'victim_id' in data and data['victim_id']:
            fields.append('victim_id')
            values.append(data['victim_id'])
        
        # Create placeholders for SQL query
        placeholders = ', '.join(['%s'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO MissingPersonReport ({field_names}) VALUES ({placeholders})"
        cursor.execute(query, tuple(values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Missing person report added successfully", "report_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/missing_persons/<int:report_id>', methods=['PUT'])
def update_missing_person(report_id):
    data = request.json if request.is_json else request.form.to_dict()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if report exists
        cursor.execute("SELECT * FROM MissingPersonReport WHERE report_id = %s", (report_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Missing person report not found"}), 404
        
        # Update the report details
        update_fields = []
        update_values = []
        
        if 'reporter_name' in data and data['reporter_name']:
            update_fields.append("reporter_name = %s")
            update_values.append(data['reporter_name'])
            
        if 'missing_person_name' in data and data['missing_person_name']:
            update_fields.append("missing_person_name = %s")
            update_values.append(data['missing_person_name'])
            
        if 'last_seen_location' in data and data['last_seen_location']:
            update_fields.append("last_seen_location = %s")
            update_values.append(data['last_seen_location'])
            
        if 'date_reported' in data and data['date_reported']:
            update_fields.append("date_reported = %s")
            update_values.append(data['date_reported'])
            
        if 'contact' in data and data['contact']:
            update_fields.append("contact = %s")
            update_values.append(data['contact'])
            
        if 'camp_id' in data:
            update_fields.append("camp_id = %s")
            update_values.append(data['camp_id'] if data['camp_id'] else None)
            
        if 'victim_id' in data:
            update_fields.append("victim_id = %s")
            update_values.append(data['victim_id'] if data['victim_id'] else None)
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
            
        query = f"UPDATE MissingPersonReport SET {', '.join(update_fields)} WHERE report_id = %s"
        update_values.append(report_id)
        
        cursor.execute(query, tuple(update_values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Missing person report updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/missing_persons/<int:report_id>', methods=['DELETE'])
def delete_missing_person(report_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if report exists
        cursor.execute("SELECT * FROM MissingPersonReport WHERE report_id = %s", (report_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Missing person report not found"}), 404
        
        # Delete the report
        cursor.execute("DELETE FROM MissingPersonReport WHERE report_id = %s", (report_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Missing person report deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Contact Form Route
@app.route('/api/contact', methods=['POST'])
def contact_form():
    data = request.json if request.is_json else request.form.to_dict()
    
    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    # In a real application, you would store this in a database and/or send an email
    # For now, we'll just return success
    return jsonify({
        "success": True, 
        "message": "Your message has been sent. Thank you!",
        "data": {
            "name": data.get('name'),
            "email": data.get('email'),
            "subject": data.get('subject')
        }
    })

# Inventory Routes
@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT i.*, c.camp_name 
            FROM Inventory i 
            LEFT JOIN ReliefCamp c ON i.camp_id = c.camp_id
        """)
        items = cursor.fetchall()
        result = convert_to_json(items, cursor)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT i.*, c.camp_name 
            FROM Inventory i 
            LEFT JOIN ReliefCamp c ON i.camp_id = c.camp_id
            WHERE i.item_id = %s
        """, (item_id,))
        item = cursor.fetchone()
        
        if not item:
            return jsonify({"success": False, "message": "Inventory item not found"}), 404
            
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, item))
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/inventory', methods=['POST'])
def add_inventory_item():
    data = request.json if request.is_json else request.form.to_dict()
    
    # Validate required fields
    required_fields = ['item_name', 'quantity']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get max item_id and increment by 1 for new record
        cursor.execute("SELECT MAX(item_id) FROM Inventory")
        max_id = cursor.fetchone()[0]
        new_id = 201 if max_id is None else max_id + 1
        
        # Get current date if not provided
        date_received = data.get('date_received', date.today().isoformat())
        
        # Build query based on available data
        fields = ['item_id', 'item_name', 'quantity', 'date_received']
        values = [new_id, data['item_name'], data['quantity'], date_received]
        
        # Optional fields
        if 'camp_id' in data and data['camp_id']:
            fields.append('camp_id')
            values.append(data['camp_id'])
        
        # Create placeholders for SQL query
        placeholders = ', '.join(['%s'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO Inventory ({field_names}) VALUES ({placeholders})"
        cursor.execute(query, tuple(values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Inventory item added successfully", "item_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    data = request.json if request.is_json else request.form.to_dict()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if item exists
        cursor.execute("SELECT * FROM Inventory WHERE item_id = %s", (item_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Inventory item not found"}), 404
        
        # Update the item details
        update_fields = []
        update_values = []
        
        if 'item_name' in data and data['item_name']:
            update_fields.append("item_name = %s")
            update_values.append(data['item_name'])
            
        if 'quantity' in data and data['quantity']:
            update_fields.append("quantity = %s")
            update_values.append(data['quantity'])
            
        if 'date_received' in data and data['date_received']:
            update_fields.append("date_received = %s")
            update_values.append(data['date_received'])
            
        if 'camp_id' in data:
            update_fields.append("camp_id = %s")
            update_values.append(data['camp_id'] if data['camp_id'] else None)
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
            
        query = f"UPDATE Inventory SET {', '.join(update_fields)} WHERE item_id = %s"
        update_values.append(item_id)
        
        cursor.execute(query, tuple(update_values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Inventory item updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if item exists
        cursor.execute("SELECT * FROM Inventory WHERE item_id = %s", (item_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Inventory item not found"}), 404
        
        # Check for related records in other tables
        cursor.execute("SELECT COUNT(*) FROM Donor WHERE item_id = %s", (item_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete item with associated donors"}), 400
            
        cursor.execute("SELECT COUNT(*) FROM Donation WHERE item_id = %s", (item_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete item with associated donations"}), 400
            
        cursor.execute("SELECT COUNT(*) FROM Supply WHERE item_id = %s", (item_id,))
        if cursor.fetchone()[0] > 0:
            return jsonify({"success": False, "message": "Cannot delete item with associated supplies"}), 400
        
        # Delete the item
        cursor.execute("DELETE FROM Inventory WHERE item_id = %s", (item_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Inventory item deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Volunteer Routes
@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Volunteer")
        volunteers = cursor.fetchall()
        result = convert_to_json(volunteers, cursor)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/volunteers/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Volunteer WHERE volunteer_id = %s", (volunteer_id,))
        volunteer = cursor.fetchone()
        
        if not volunteer:
            return jsonify({"success": False, "message": "Volunteer not found"}), 404
            
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, volunteer))
        
        # Get volunteer assignments
        cursor.execute("""
            SELECT va.*, rc.camp_name 
            FROM VolunteerAssignment va 
            JOIN ReliefCamp rc ON va.camp_id = rc.camp_id
            WHERE va.volunteer_id = %s
        """, (volunteer_id,))
        assignments = cursor.fetchall()
        result['assignments'] = convert_to_json(assignments, cursor)
        
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/volunteers', methods=['POST'])
def add_volunteer():
    data = request.json if request.is_json else request.form.to_dict()
    
    # Validate required fields
    required_fields = ['first_name', 'last_name', 'contact_number']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get max volunteer_id and increment by 1 for new record
        cursor.execute("SELECT MAX(volunteer_id) FROM Volunteer")
        max_id = cursor.fetchone()[0]
        new_id = 401 if max_id is None else max_id + 1
        
        # Build query based on available data
        fields = ['volunteer_id', 'first_name', 'last_name', 'contact_number']
        values = [new_id, data['first_name'], data['last_name'], data['contact_number']]
        
        # Optional fields
        if 'skills' in data and data['skills']:
            fields.append('skills')
            values.append(data['skills'])
        
        # Create placeholders for SQL query
        placeholders = ', '.join(['%s'] * len(fields))
        field_names = ', '.join(fields)
        
        query = f"INSERT INTO Volunteer ({field_names}) VALUES ({placeholders})"
        cursor.execute(query, tuple(values))
        
        # Add volunteer assignment if provided
        if 'camp_id' in data and data['camp_id']:
            # Get max assignment_id
            cursor.execute("SELECT MAX(assignment_id) FROM VolunteerAssignment")
            max_assignment_id = cursor.fetchone()[0]
            new_assignment_id = 101 if max_assignment_id is None else max_assignment_id + 1
            
            # Set default dates if not provided
            start_date = data.get('start_date', date.today().isoformat())
            end_date = data.get('end_date', None)
            
            cursor.execute(
                "INSERT INTO VolunteerAssignment (assignment_id, volunteer_id, camp_id, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
                (new_assignment_id, new_id, data['camp_id'], start_date, end_date)
            )
        
        conn.commit()
        
        return jsonify({"success": True, "message": "Volunteer added successfully", "volunteer_id": new_id})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/volunteers/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    data = request.json if request.is_json else request.form.to_dict()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if volunteer exists
        cursor.execute("SELECT * FROM Volunteer WHERE volunteer_id = %s", (volunteer_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Volunteer not found"}), 404
        
        # Update the volunteer details
        update_fields = []
        update_values = []
        
        if 'first_name' in data and data['first_name']:
            update_fields.append("first_name = %s")
            update_values.append(data['first_name'])
            
        if 'last_name' in data and data['last_name']:
            update_fields.append("last_name = %s")
            update_values.append(data['last_name'])
            
        if 'contact_number' in data and data['contact_number']:
            update_fields.append("contact_number = %s")
            update_values.append(data['contact_number'])
            
        if 'skills' in data:
            update_fields.append("skills = %s")
            update_values.append(data['skills'] if data['skills'] else None)
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
            
        query = f"UPDATE Volunteer SET {', '.join(update_fields)} WHERE volunteer_id = %s"
        update_values.append(volunteer_id)
        
        cursor.execute(query, tuple(update_values))
        conn.commit()
        
        return jsonify({"success": True, "message": "Volunteer updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/volunteers/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if volunteer exists
        cursor.execute("SELECT * FROM Volunteer WHERE volunteer_id = %s", (volunteer_id,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "Volunteer not found"}), 404
        
        # Delete associated assignments first
        cursor.execute("DELETE FROM VolunteerAssignment WHERE volunteer_id = %s", (volunteer_id,))
        
        # Delete the volunteer
        cursor.execute("DELETE FROM Volunteer WHERE volunteer_id = %s", (volunteer_id,))
        conn.commit()
        
        return jsonify({"success": True, "message": "Volunteer deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
