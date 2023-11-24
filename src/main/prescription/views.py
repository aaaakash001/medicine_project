from flask import request, jsonify, render_template
from src.main.utils import get_medicine_data
from src.main.prescription import prescription_bp


@prescription_bp.route('/prescription')
def prescription():
    return render_template('prescription.html')


# suggestion on search bar while searching for composition.
@prescription_bp.route('/prescription-suggest', methods=['GET'])
def prescription_suggest():
    global conn
    search_term = request.args.get('term')

    # Query the database using SQLAlchemy
    suggestions = get_medicine_data(
        search_term=search_term,
        columns=['id', 'composition'])
    return jsonify(suggestions)
