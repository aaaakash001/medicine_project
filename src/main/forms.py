from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('Search for Medicine Compositions',
                        name='search', validators=[
                            DataRequired(message='Enter something to search')])
    submit = SubmitField('Search', name='submit')
