from flask import Blueprint, render_template, jsonify, request
from backend.db import conn


analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analysis')
def analysis():
    return render_template('analysis.html')

# to search for composition and fetch
# name,composition ,brand, type, price from database


@analysis_bp.route('/analysis-search', methods=['POST'])
def analysis_search():
    global conn
    search_term = request.form['composition']
    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Query the database
    cur.execute(
        "SELECT name,composition ,brand, type, price FROM medicine WHERE composition = %s order by composition", (f'{search_term}',))
    result = cur.fetchall()
    print("length of result ", len(result), "Type of result", type(result))
    conn.close()
    if len(result) > 5:
        return jsonify(result)
    else:
        # If there are fewer than 5 suggestions, return an empty list or a message
        return jsonify([])


# suggestion on search bar while searching for composition.
@analysis_bp.route('/analysis-suggest', methods=['GET'])
def analysis_suggest():
    global conn
    search_term = request.args.get('term')

    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Fetch suggestions based on user input
    cur.execute("""
        SELECT composition, COUNT(*) as medicine_count
        FROM medicine
        WHERE composition ILIKE %s
        GROUP BY composition
        HAVING COUNT(*) > 5
        ORDER BY composition
    """, (f'%{search_term}%',))

    suggestions = [row[0] for row in cur.fetchall()]

    conn.close()

    return jsonify(suggestions)
