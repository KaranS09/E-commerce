from re import L
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from website.models import User

class LoginForm(FlaskForm):

 def validate_username(self, username_to_check):
  user = User.query.filter_by(username = username_to_check.data).first()
  if user:
   raise ValidationError('Username aldready exists!, Please try a different username')

 def validate_email_address(self, email_address_to_check):
  email_address = User.query.filter_by(email_address = email_address_to_check.data).first()

  if email_address:
   raise ValidationError('Email Address aldready exists! Please try a different email address')

 def validate_phone_number(self, phone_number_to_check):
  phone_number = User.query.filter_by(phone_number = phone_number_to_check.data).first()

  if phone_number:
   raise ValidationError('Phone number aldready exists! Please try a different email address')


 username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
 email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
 phone_number = StringField(label='Phone Number', validators=[Length(min=10,max=12), DataRequired(), Regexp(regex='^[+-]?[0-9]+$')])
 password1 = PasswordField(label = 'Password', validators=[Length(min=6), DataRequired()])
 password2 = PasswordField(label = 'Confirm Password', validators=[EqualTo('password1'), DataRequired()])
 address = StringField(label = 'Address (all deliveries will be done to this address)', validators=[Length(min=20), DataRequired()])
 submit = SubmitField(label='Create Account')

class SignInForm(FlaskForm):
  username = StringField(label = 'User Name', validators=[DataRequired()])
  password = PasswordField(label = 'Password', validators=[DataRequired()])
  submit = SubmitField(label = 'Sign In')

class PurchaseItemForm(FlaskForm):
  submit = SubmitField(label='Buy')
  bquantity = DecimalField(label='How many kgs', validators=[DataRequired()])

class SellItemForm(FlaskForm):
  submit = SubmitField(label='Sell')
  bquantity = DecimalField(label='How many kgs', validators=[DataRequired()])