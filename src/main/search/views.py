from flask import jsonify, request
from src import db
from src.main.utils import get_medicine_data
from src.main.models import Medicine
from src.main.search import search_bp  # Import the prescription blueprint


@search_bp.route('/search', methods=['POST'])
def search():
    search_term = request.form['composition']
    results = get_medicine_data(search_term=search_term)

    return jsonify(results)


@search_bp.route('/suggest', methods=['GET'])
def suggest():
    search_term = request.args.get('term')
    suggestions = get_medicine_data(
        search_term=search_term,
        columns=['id', 'composition']
    )
    return jsonify(suggestions)


@search_bp.route('/add_medicine', methods=['POST'])
def add_medicine():
    try:
        name = request.form['name']
        composition = request.form['composition']
        brand = request.form['brand']
        type = request.form['type']
        price = str(request.form['price'])  # Assuming price is a float
        prescription_required = request.form.get('prescription') == "on"

        # Create a new Medicine instance and add it to the database
        new_medicine = Medicine(
            name=name,
            composition=composition,
            brand=brand,
            type=type,
            price=price,
            prescription_required=prescription_required
        )

        db.session.add(new_medicine)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Medicine added successfully.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error: ' + str(e)
        })


@search_bp.route('/add_medicines', methods=['POST'])
def add_medicines():
    return jsonify({'success': False, 'message': 'Not implemented.'})
