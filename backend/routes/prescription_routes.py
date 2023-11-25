import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from backend.db import engine

prescription_bp = Blueprint('prescription', __name__)


def fetch_unique_compositions_from_db():
    query = "SELECT DISTINCT composition FROM medicine"
    compositions = pd.read_sql(query, con=engine)
    return compositions['composition'].tolist()


@prescription_bp.route('/prescription')
def prescription():
    compositions = fetch_unique_compositions_from_db()
    return render_template('prescription.html', compositions=compositions)

# suggestion on search bar while searching for composition.


@prescription_bp.route('/prescription-suggest', methods=['GET'])
def prescription_suggest():
    global conn
    search_term = request.args.get('term')

    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Fetch suggestions based on user input
    cur.execute("""
        SELECT composition as medicine_count
        FROM medicine
        WHERE composition ILIKE %s
        ORDER BY composition
    """, (f'%{search_term}%',))

    suggestions = [row[0] for row in cur.fetchall()]

    conn.close()

    return jsonify(suggestions)
