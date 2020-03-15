from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class LeaveForm(FlaskForm):
    username = StringField('Username', render_kw={'disabled':''})
    facultyusername = StringField('Faculty username: ', render_kw={'disabled':''})
    fromdate = DateField('From (yyyy-mm-dd): ', validators=[DataRequired()])
    todate = DateField('To (yyyy-mm-dd): ', validators=[DataRequired()])
    reason = StringField('Reason: ', validators=[DataRequired()])
    typeofleave = SelectField(
        'Type of Leave : ',
        choices=[('ML', 'Medical Leave'), ('OD', 'On Duty'), ('OL', 'Ordinary Leave')]
    )
    leavestatus = HiddenField('Leave Status', default = 'Pending')
    submit = SubmitField('Apply Leave')