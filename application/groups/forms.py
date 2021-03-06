from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class GroupForm(FlaskForm):
    name = StringField("Group name", [validators.Length(min=2, max=20)])
 
    class Meta:
        csrf = False