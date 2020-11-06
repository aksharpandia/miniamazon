from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, SubmitField, BooleanField, FloatField, PasswordField
from wtforms.validators import DataRequired, InputRequired, Regexp, ValidationError
from models import *

class SearchForm(FlaskForm):
    search = StringField('search', [DataRequired()])
#   submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})

class AddProductForm(FlaskForm):
    productName = StringField('Product Name')
    modelNum = IntegerField('Model Number', validators=[InputRequired()])
    productDescription = StringField('Product Description')
    productImage = FileField('Product Image', validators=[Regexp('[^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$')])
    stock = IntegerField('How many are you (re)stocking?')
    isRecommended = BooleanField('Should This Be Recommended') #just added this cuz it's required for some reason
    price = FloatField('Price of the Product') # nullable=false so should this be inputrequired?
    submit = SubmitField('Add Product(s)')

class AddBuyerForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    balance = FloatField('Balance', validators=[InputRequired()])
    shippingAddress = StringField('Shipping Address', validators=[InputRequired()])
    billingAddress = StringField('Billing Address', validators=[InputRequired()])
    photo = FileField('User Image', validators=[Regexp('[^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$')])
    submit = SubmitField('Finish Account Setup')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            print('same name')
            raise ValidationError('This name is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')

class AddSellerForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    submit = SubmitField('Finish Account Setup')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            print('same name')
            raise ValidationError('This name is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')

class AddCartForm(FlaskForm):
    cartID = IntegerField('ID', validators=[InputRequired()])
    buyerID = IntegerField('ID', validators=[InputRequired()])
    modDateTime = StringField('Modified Date', validators=[InputRequired()])
    submit = SubmitField('Add Cart')

class AddOrderForm(FlaskForm):
    orderID = IntegerField('Order ID (auto-generated)', validators=[InputRequired()])
    buyerID = IntegerField("Buyer ID (would be auto-completed based on buyer's cart)", validators=[InputRequired()])
    transacAmount = FloatField('Transaction Amount', validators=[InputRequired()])
    deliveryOption = StringField('Delivery Option', validators=[InputRequired()])
    createdDateTime = StringField('Created Date', validators=[InputRequired()])
    submit = SubmitField('Add Order')

class AddReviewsForm(FlaskForm):
    reviewsID = IntegerField('ID of Review', validators=[InputRequired()])
    rating = IntegerField('Rating', validators=[InputRequired()])    
    headline = StringField('Headline for your review', validators=[InputRequired()])  
    commentary = StringField('Your feedback', validators=[InputRequired()])  
    dateReviewed = StringField('Date Today', validators=[InputRequired()])
    userID = IntegerField('Your User ID', validators=[InputRequired()])
    modelNum = IntegerField('Model Number', validators=[InputRequired()])
    submit = SubmitField('Submit Review')

class LogInForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddBalanceForm(FlaskForm):
    newbalance = FloatField('Add To Balance By', validators=[InputRequired()])
    submit = SubmitField('Add Balance')
