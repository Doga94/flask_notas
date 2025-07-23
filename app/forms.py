from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NoteForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired()])
    content = StringField("Contenido", validators=[DataRequired()])
    submit = SubmitField("Guardar")