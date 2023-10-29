from flask import Flask, render_template, request
import psycopg2
from flask import jsonify
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px



app = Flask(__name__)

app_dash = Dash(__name__, server=app, url_base_pathname='/dashboard/')

df = pd.read_csv('/Users/akashagarwal/Downloads/IIT Bombay/CS 699 Software lab/medicine project/medicine_all.csv')


#['Medicine Name', 'Manufacturer', 'Medicine Type', 'Active Ingredient', 'MRP', 'Prescription Required'] 

app_dash.layout = html.Div([
    dcc.Dropdown(
        id='composition-dropdown',
        options=[
            {'label': composition, 'value': composition}
            for composition in df['Active Ingredient'].unique()
        ],
        value=df['Active Ingredient'].unique()[0]
    ),
    dcc.Graph(id='bar-chart')
])

@app_dash.callback(
    Output('bar-chart', 'figure'),
    Input('composition-dropdown', 'value')
)
def update_histogram(selected_composition):
    filtered_df = df[df['Active Ingredient'] == selected_composition]
    fig = px.bar(filtered_df, x='Manufacturer', y='MRP')
    return fig









# Configure your PostgreSQL database connection
db_config = {
    'dbname': 'postgres',
    'user': '',
    'password': '',
    'host': 'localhost',
    'port': '5431',
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bill')
def bill():
    return render_template('bill.html')


#////////////////////////////////////////////////////////
#admin-dashboard
@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/add_medicine', methods=['POST'])
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
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Insert data into the medicine table
        cur.execute('INSERT INTO medicine (name, composition, brand, type, price, "prescription required") VALUES (%s, %s, %s, %s, %s, %s)',
                    (name, composition, brand, type, price, prescription_required))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Medicine added successfully.'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error: ' + str(e)})


#////////////////////////////////////////////////////////



#/////////////////////
#admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin-search', methods=['POST'])
def admin_search():
    data = request.get_json()  # Retrieve JSON data from the request body
    search_term = data['username']
    search_password = data['password']
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT username, password FROM admin WHERE username = %s", (f'{search_term}',))
    result = cur.fetchone()
    conn.close()
    print(result)
    if result and result[1] == search_password:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


#////////////////

@app.route('/prescription')
def prescription():
    return render_template('prescription.html')


@app.route('/brands')
def brands():
    return render_template('brands.html')


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
    return jsonify(result)





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




"""
analysis page
"""
@app.route('/analysis-search', methods=['POST'])
def analysis_search():
    search_term = request.form['composition']
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT name,composition ,brand, type, price FROM medicine WHERE composition = %s order by composition", (f'{search_term}',))
    result = cur.fetchall()
    print("length of result ",len(result), "Type of result", type(result))
    conn.close()
    if len(result) > 5:
        return jsonify(result)
    else:
        # If there are fewer than 5 suggestions, return an empty list or a message
        return jsonify([])

@app.route('/analysis-suggest', methods=['GET'])
def analysis_suggest():
    search_term = request.args.get('term')

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Fetch suggestions based on user input (modify this query to match your database structure)
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


@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

#//////////////////




if __name__ == '__main__':
    app.run(debug=True)
