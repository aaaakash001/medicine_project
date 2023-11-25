import traceback
from flask import Blueprint, render_template, jsonify, request
from backend.db import conn


bill_bp = Blueprint('bill', __name__)

@bill_bp.route('/bill')
def bill():
    return render_template('bill.html')


# suggestion on search bar while searching for composition.
@bill_bp.route('/composition-suggest', methods=['GET'])
def composition_suggest():
    global conn
    search_term = request.args.get('term')

    try:
        # Connect to the PostgreSQL database
        cur = conn.cursor()

        # Fetch suggestions based on user input
        cur.execute("""
            SELECT DISTINCT composition
            FROM medicine
            WHERE composition ILIKE %s 
            ORDER BY composition 
        """, (f'%{search_term}%',))
        
        suggestions = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"Error in composition_suggest: {e}")
        traceback.print_exc()  # Print the traceback for debugging
        suggestions = []
    finally:
        cur.close()

    return jsonify(suggestions)


@bill_bp.route('/medicines', methods=['GET'])
def get_medicines():
    try:
        # Connect to the PostgreSQL database
        cur = conn.cursor()

        # Get the selected composition from the request parameters
        selected_composition = request.args.get('composition')
        print(selected_composition)
        # Fetch medicines based on the selected composition (exact match)
        cur.execute("""
            SELECT name,price
            FROM medicine
            WHERE composition ILIKE %s
            ORDER BY name
        """, (f'%{selected_composition}%',))

        medicines = ["Medicine: "+row[0] +"| Price: "+str(row[1]) for row in cur.fetchall()]
        print(medicines)
    except Exception as e:
        print(f"Error in get_medicines: {e}")
        traceback.print_exc()  # Print the traceback for debugging
        medicines = []
    finally:
        cur.close()

    return jsonify(medicines)

