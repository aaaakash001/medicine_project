from flask import render_template, jsonify, request
from src.main import main_bp
from src.main.prescription import prescription_bp
from src.main.analysis import analysis_bp
from src.main.search import search_bp
from src.main.bill import bill_bp
from src.main.brands import brands_bp
from werkzeug.security import check_password_hash
from src.auth.models import User
from src.main.utils import allowed_file, insert_from_csv_to_db


# index or main page
@main_bp.route('/')
def index():
    return render_template('index.html')


# admin-dashboard
@main_bp.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


# admin page
@main_bp.route('/admin')
def admin():
    return render_template('admin.html')


@main_bp.route('/admin-search', methods=['POST'])
def admin_search():
    data = request.get_json()  # Retrieve JSON data from the request body
    search_term = data['username']
    search_password = data['password']
    
    user = User.query.filter_by(username=search_term).first()

    if user and check_password_hash(
            user.password_hash,
            search_password
        ):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@main_bp.route('/admin-upload', methods=['POST'])
def admin_upload_csv():
    if('file' in request.files):
        file = request.files['file']
        if (file and file.filename != '' and allowed_file(file.filename)):
            res, err = insert_from_csv_to_db(file.stream, is_stream=True)
    if (res is None):
        return render_template('admin_dashboard.html', csv_upload_message='File not received')
    elif (err is not None):
        return render_template('admin_dashboard.html', csv_upload_message=err)
    else:
        return render_template('admin_dashboard.html', csv_upload_message='Inserted into database')


main_bp.register_blueprint(prescription_bp, url_prefix='/prescription')
main_bp.register_blueprint(analysis_bp, url_prefix='/analysis')
main_bp.register_blueprint(search_bp, url_prefix='/search')
main_bp.register_blueprint(bill_bp, url_prefix='/bill')
main_bp.register_blueprint(brands_bp, url_prefix='/brands')
