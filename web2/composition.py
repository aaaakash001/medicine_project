from flask import Flask, render_template, request
import psycopg2
from flask import jsonify


app = Flask(__name__)

# Configure your PostgreSQL database connection
db_config = {
    'dbname': 'postgres',
    'user': '',
    'password': '',
    'host': 'localhost',
    'port': '5433',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['composition']

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT name,composition ,brand, type, price FROM medicine WHERE composition ILIKE %s order by composition", (f'%{search_term}%',))
    result = cur.fetchall()

    conn.close()

    return render_template('results.html', data=result)

@app.route('/suggest', methods=['GET'])
def suggest():
    search_term = request.args.get('term')

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Fetch suggestions based on user input (modify this query to match your database structure)
    cur.execute("SELECT distinct composition FROM medicine WHERE composition ILIKE %s order by composition", (f'%{search_term}%',))
    suggestions = [row[0] for row in cur.fetchall()]

    conn.close()

    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
