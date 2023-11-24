import csv
import sqlalchemy
from src import db
from src.main.models import Medicine


def get_medicine_data(
        search_term: str = None,
        search_column: str = None,
        columns: list[str] = None,
        distinct: bool = False,
        similar: bool = True,
        group_by: str = None,
        having_func: sqlalchemy.sql.elements.BinaryExpression = None,
        order_by: list[tuple[str, bool]] = None, # [(column:str, asc:bool(True))],
        limit: int = None,
) -> list[dict]:
    # Query the database using SQLAlchemy
    query = Medicine.query
    valid_columns = []

    if (columns is not None):
        # Check for valid columns
        valid_columns = [
            getattr(Medicine, col)
            for col in columns
            if hasattr(Medicine, col)
        ]
        query = query.with_entities(*valid_columns)

    if (distinct):
        query = query.distinct(*valid_columns)

    if (search_term is not None and search_column is not None):
        if (hasattr(Medicine, search_column)):
            if (similar):
                query.filter(
                    getattr(Medicine, search_column).ilike(f'%{search_term}%'))
            else:
                query.filter(getattr(Medicine, search_column) == search_term)

    if (group_by is not None and hasattr(Medicine, group_by)):
        query = query.group_by(getattr(Medicine, group_by))

    if (having_func is not None):
        query = query.having(having_func)

    if (order_by):
        for order in order_by:
            if (hasattr(Medicine, order[0])):
                orderByAttribute = getattr(Medicine, order[0])
                query = query.order_by(
                    orderByAttribute.desc()
                    if order[1] else orderByAttribute.asc()
                )

    if limit is not None:
        query = query.limit(limit)

    queryResults = query.all()

    # Safe Check SQLAlchemy -> list[dict]
    return [{
            col: getattr(result, col) for col in columns} for
            result in
            queryResults] if columns else queryResults


def insert_from_csv_to_db(csv_file_path, table_name):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        rows = []
        for row in reader:
            # Convert empty strings to None for NULL values in the database
            row = [value if value != '' else None for value in row]
            rows.append(dict(zip(header, row)))

        # Use bulk_insert_mappings to insert rows in bulk
        with db.engine.connect() as connection:
            connection.execute(Medicine.__table__.insert().values(rows))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {
        'csv'
    }
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS
