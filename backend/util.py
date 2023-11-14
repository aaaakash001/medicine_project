import csv
from psycopg2 import sql
from db import conn

def insert_from_csv_to_db(csv_file_path, table_name):
    cursor = conn.cursor()

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)

        insertQuery = sql.SQL("INSERT INTO medicine ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, header)),
            sql.SQL(', ').join(sql.Placeholder() * len(header))
        )

        for row in reader:
            # Convert empty strings to None for NULL values in the database
            row = [value if value != '' else None for value in row]

            cursor.execute(insertQuery, row)

    # Commit and close resources
    conn.commit()
    cursor.close()
    conn.close()