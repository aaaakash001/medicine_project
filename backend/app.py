from flask import Flask, render_template, request
from flask import jsonify
from dash import Dash, html, dcc
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_table
from db import engine, conn

app = Flask(__name__,static_folder="static")

#//////////////////////////////////////////////////////////////////
# Dash initialize composition across brands analysis
dashApp = Dash(__name__, server=app, url_base_pathname='/composition/')

# Function to fetch unique compositions from the database
def fetch_unique_compositions_from_db():
    query = "SELECT DISTINCT composition FROM medicine"
    compositions = pd.read_sql(query, con=engine)
    return compositions['composition'].tolist()

# Defining layout
dashApp.layout = html.Div([
    dcc.Dropdown(
        id='composition-dropdown',
        options=[
            {'label': composition, 'value': composition}
            for composition in fetch_unique_compositions_from_db()
        ],
        value=fetch_unique_compositions_from_db()[0]
    ),
    
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in [ 'brand', 'name','type', 'price']],
        style_data={'textAlign': 'center'},
    ),
    dcc.Graph(id='bar-chart')
])

# Define the update_histogram function
@dashApp.callback(
    [Output('bar-chart', 'figure'),
     Output('table', 'data')],
    Input('composition-dropdown', 'value')
)
def update_histogram(selectedComposition):
    # Construct the SQL query with placeholders for user inputs
    query = "SELECT  brand,name, type, price FROM medicine WHERE composition = %s order by brand"
    
    # Use the SQLAlchemy engine to execute the query and pass the parameters
    df = pd.read_sql(query, con=engine, params=(selectedComposition,))
    
    # Create the bar chart
    fig = px.bar(df, x='brand', y='price', labels={'price': 'Price'})

    return fig, df.to_dict('records')

#////////////////////////////////////////////////////////////////////////////////////////////

brands = Dash(__name__, server=app, url_base_pathname='/brands/')

# Function to fetch unique compositions from the database
def fetch_unique_brands_from_db():
    query = "SELECT DISTINCT brand FROM medicine"
    brand = pd.read_sql(query, con=engine)
    return brand['brand'].tolist()

# Defining layout
brands.layout = html.Div([
    dcc.Dropdown(
        id='brand-dropdown',
        options=[
            {'label': brand, 'value': brand}
            for brand in fetch_unique_brands_from_db()
        ],
        value=fetch_unique_brands_from_db()[0]
    ),
    
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in [ 'name', 'composition','type', 'price']],
        style_data={'textAlign': 'center'},
    ),
    dcc.Graph(id='bar-chart')
])

# Define the update_histogram function
@brands.callback(
    [Output('bar-chart', 'figure'),
     Output('table', 'data')],
    Input('brand-dropdown', 'value')
)
def update_histogram_brands(selectedBrands):
    # Construct the SQL query with placeholders for user inputs
    query = "SELECT  name,composition, type, price FROM medicine WHERE brand = %s order by name"
    
    # Use the SQLAlchemy engine to execute the query and pass the parameters
    df = pd.read_sql(query, con=engine, params=(selectedBrands,))
    
    # Create the bar chart
    fig = px.scatter(df, x='composition', y='price', labels={'price': 'Price'})

    return fig, df.to_dict('records')



















#index or main page
@app.route('/')
def index():
    return render_template('index.html')

#//////////////////////////////////////////////////////
#bill-page
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
    global conn
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
#admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin-search', methods=['POST'])
def admin_search():
    global conn
    data = request.get_json()  # Retrieve JSON data from the request body
    search_term = data['username']
    search_password = data['password']
    # Connect to the PostgreSQL database
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


#//////////////////////////////////////////////////////////
#prescription-page
@app.route('/prescription')
def prescription():
    return render_template('prescription.html')

# suggestion on search bar while searching for composition.
@app.route('/prescription-suggest', methods=['GET'])
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



#//////////////////////////////////////////////////////////
#brands-page
@app.route('/brands')
def brands():
    return render_template('brands.html')


@app.route('/search', methods=['POST'])
def search():
    global conn
    search_term = request.form['composition']
    
    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Query the database
    cur.execute("SELECT name,composition ,brand, type, price FROM medicine WHERE composition ILIKE %s order by composition", (f'%{search_term}%',))
    result = cur.fetchall()

    conn.close()
    return jsonify(result)





@app.route('/suggest', methods=['GET'])
def suggest():
    global conn
    search_term = request.args.get('term')

    # Connect to the PostgreSQL database
    cur = conn.cursor()

    # Fetch suggestions based on user input
    cur.execute("SELECT distinct composition FROM medicine WHERE composition ILIKE %s order by composition", (f'%{search_term}%',))
    suggestions = [row[0] for row in cur.fetchall()]

    conn.close()

    return jsonify(suggestions)




#//////////////////////////////////////////////////////////
#analysis-page

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# to search for composition and fetch
# name,composition ,brand, type, price from database

@app.route('/analysis-search', methods=['POST'])
def analysis_search():
    global conn
    search_term = request.form['composition']
    # Connect to the PostgreSQL database
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


# suggestion on search bar while searching for composition.
@app.route('/analysis-suggest', methods=['GET'])
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



#/////////////////////////////////////////////////
if __name__ == '__main__':
    app.run(debug=True)
