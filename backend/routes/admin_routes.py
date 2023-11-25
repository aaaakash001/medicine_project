from flask import Blueprint, render_template, jsonify, request
from backend.db import conn

admin_bp = Blueprint('admin', __name__)

#admin page
@admin_bp.route('/admin')
def admin():
    return render_template('admin.html')

@admin_bp.route('/admin-search', methods=['POST'])
def admin_search():
    data = request.get_json()  # Retrieve JSON data from the request body
    search_term = data['username']
    search_password = data['password']
    # Connect to the PostgreSQL database
    connection = conn
    cur = connection.cursor()

    # Query the database
    cur.execute("SELECT username, password FROM users WHERE username = %s", (f'{search_term}',))
    result = cur.fetchone()
    print(result)
    if result and result[1] == search_password:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


#admin-dashboard
@admin_bp.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/add_medicine', methods=['POST'])
def add_medicine():
    try:
        name = request.form['name']
        composition = request.form['composition']
        brand = request.form['brand']
        type = request.form['type']
        price = str(request.form['price'])  # Assuming price is a float
        prescription_required = "false"  # Check if the checkbox is checked
        if(request.form.get('prescription') == "on"):
            prescription_required = "true"
      
        
        # Connect to the PostgreSQL database (db_config)
        connection = conn
        cur = connection.cursor()

        # Insert data into the medicine table
        cur.execute('INSERT INTO medicine (name, composition, brand, type, price, prescription) VALUES (%s, %s, %s, %s, %s, %s)',
                    (name, composition, brand, type, price, prescription_required))

        conn.commit()

        return jsonify({'success': True, 'message': 'Medicine added successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error: ' + str(e)})

