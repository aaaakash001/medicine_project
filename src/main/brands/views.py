from flask import request, jsonify, render_template
from src.main.utils import get_medicine_data
from src.main.brands import brands_bp


@brands_bp.route('/brands')
def brands():
    return render_template('brands.html')


# suggestion on search bar while searching for composition.
@brands_bp.route('/suggest', methods=['GET'])
def suggest():
    search_term = request.args.get('term')

    # Query the database using SQLAlchemy
    suggestions = get_medicine_data(
        search_term=search_term,
        columns=['id','name','composition' ,'brand', 'type','price'])
    return jsonify(suggestions)

# suggestion on search bar while searching for composition.
@brands_bp.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('term')

    # Query the database using SQLAlchemy
    suggestions = get_medicine_data(
        search_term=search_term,
        columns=['id', 'composition'], distinct=True)
    return jsonify(suggestions)