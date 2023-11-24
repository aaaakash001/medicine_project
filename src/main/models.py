from src import db


class Medicine(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    brand = db.Column(db.String(200), primary_key=True)
    type = db.Column(db.String(200), primary_key=True)
    composition = db.Column(db.String(200), primary_key=True)
    price = db.Column(db.Float, nullable=False)
    prescription_required = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Medicine {self.name}>'
