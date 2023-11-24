import traceback
from flask import request, jsonify, render_template
from src.main.utils import get_medicine_data
from src.main.bill import bill_bp


@bill_bp.route('/bill')
def bill():
    return render_template('bill.html')


# suggestion on search bar while searching for composition.
@bill_bp.route('/composition-suggest', methods=['GET'])
def composition_suggest():
    search_term = request.args.get('term')

    # Query the database using SQLAlchemy
    suggestions = get_medicine_data(
        search_term=search_term, 
        columns=['id', 'composition'],distinct=True)
    return jsonify(suggestions)


@bill_bp.route('/medicines', methods=['GET'])
def get_medicines():
    selected_composition = request.args.get('composition')
    
    suggestions = get_medicine_data(
         search_term=selected_composition, 
        columns=['id', 'name','price'])
    
    medicines = ["Medicine: "+row[0] +"| Price: "+str(row[1]) for row in suggestions]

    return jsonify(medicines)