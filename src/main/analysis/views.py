from flask import render_template, request, jsonify
from sqlalchemy import func
from src.main.utils import get_medicine_data
from src.main.analysis import analysis_bp  # Import the prescription blueprint


@analysis_bp.route('/analysis')
def analysis():
    return render_template('analysis.html')


# to search for composition and fetch
# name,composition ,brand, type, price from database
@analysis_bp.route('/analysis-search', methods=['POST'])
def analysis_search():
    search_term = request.form['composition']
    results = get_medicine_data(
        search_term=search_term,
        limit=5,
        distinct=True,
        similar=False)
    if len(results) > 5:
        return jsonify(results)
    else:
        # If there are fewer than 5 suggestions,
        # return an empty list or a message
        return jsonify([])


# suggestion on search bar while searching for composition.
@analysis_bp.route('/analysis-suggest', methods=['GET'])
def analysis_suggest():
    search_term = request.args.get('term')
    suggestions = get_medicine_data(
        search_term=search_term,
        columns=['composition'],
        distinct=True,
        similar=True,
        group_by='composition',
        having_func=(func.count() > 5),
        limit=5,
        order_by=[('composition', False)]
    )
    return jsonify(suggestions)
