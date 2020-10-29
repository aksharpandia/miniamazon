from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

# loading the env
load_dotenv('.env')

app = Flask(__name__)

# configuring the database 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

# for login purposes
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# importing the models and forms
from forms import *
from models import *

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.route('/')
@login_required
def main():
    return render_template('index.html')

def create_user_cart(userID, type, new=False):
    if type != "buyer":
        return
    rand_cartID = randint(0,999999) # Need to adjust later
    temp_modDateTime = "2020-10-17"
    cart = Cart(rand_cartID, userID, temp_modDateTime)
    cart.cartID = rand_cartID
    cart.buyerID = userID
    cart.modDateTime = temp_modDateTime
    if new:
        db.session.add(cart)
    db.session.commit()

@app.route('/seller/<seller_id>')
def seller_id(seller_id):
    return render_template('seller-product.html', 
        curr_seller=User.query.filter(User.id == seller_id).one(), 
        products=Product.query.filter(Product.userID == seller_id))

@app.route('/buyer')
def buyer():
    return render_template('buyer.html', buyers=Buyer.query.all())

@app.route('/product')
def product():
    return render_template('product.html', products=Product.query.all())

@app.route('/add-product/<seller_id>', methods=['GET', 'POST'])
def addProduct(seller_id):
    form = AddProductForm()
    if request.method=='POST': # need to validate form
        product = Product(form.productName.data, form.modelNum.data, current_user.id,
                        form.productDescription.data, form.productImage.data, form.stock.data, form.isRecommended.data,
                        form.price.data)
        save_product_add(product, form, new=True)
        flash(f'You added {form.stock.data} {form.productName.data} product(s)!', 'success')
        return redirect('/seller/' + str(seller_id))
    return render_template('add-product.html', title='Add to Your Product Listings', form=form)

def save_product_add(product, form, new=False):
    """
    Save adding the product to the database
    """
    # Get data from form and assign it to the correct attributes of the SQLAlchemy table object

    # data from the user input
    product.productName = form.productName.data
    product.modelNum = form.modelNum.data
    product.userID = current_user.id # this needs to match the id of a seller due to foreign key constraint
    product.productDescription = form.productDescription.data
    product.productImage = form.productImage.data
    product.stockLeft += form.stock.data
    product.price = form.price.data

    if new:
        db.session.add(product)
    db.session.commit()

@app.route('/add-order', methods=['GET', 'POST'])
def addOrder():
    form = AddOrderForm()
    if request.method=='POST': # need to validate form
        order = Order(form.orderID.data, form.buyerID.data, form.transacAmount.data, 
            form.deliveryOption.data, form.createdDateTime.data)
        save_order_add(order, form, new=True)
        flash(f'You created order {form.orderID.data} for ${form.transacAmount.data}', 'success')
        return redirect(url_for('order')) # redirect to cart page so they can see the updated table
    return render_template('add-order.html', title='Add to Your Orders', form=form)

def save_order_add(order, form, new=False):
    order.orderID = form.orderID.data
    order.buyerID = form.buyerID.data
    order.transacAmount = form.transacAmount.data
    order.deliveryOption = form.deliveryOption.data 
    order.createdDateTime = form.createdDateTime.data

    if new:
        db.session.add(order)
    db.session.commit()


@app.route('/delete_product/<seller_id>/<product_id>', methods=['GET', 'POST'])
def deleteProduct(seller_id, product_id):
    if request.method == 'POST':
        prodToDelete = Product.query.filter(Product.modelNum == product_id, Product.userID == seller_id).first()
        db.session.delete(prodToDelete)
        db.session.commit()
        flash(
            f'You successfully deleted {prodToDelete.productName}!', 'success')
        return redirect('/seller/' + str(seller_id))

@app.route('/update_product/<seller_id>/<product_id>',  methods=['GET', 'POST'])
def updateProduct(seller_id, product_id):
    form = AddProductForm()
    prodToUpdate = Product.query.filter(
        Product.modelNum == product_id, Product.userID == seller_id).first()
    
    if request.method == 'POST':
        flash(f'You successfully updated {prodToUpdate.productName}!', 'success')
        save_product_add(prodToUpdate, form, new=False)
        return redirect('/seller/' + str(seller_id))
    elif request.method == 'GET':
        fillOutProductFields(prodToUpdate, form)
    return render_template('add-product.html', title='Update Your Product', form=form)


def fillOutProductFields(product, form):
    form.productName.data = product.productName 
    form.modelNum.data = product.modelNum
    form.productDescription.data = product.productDescription 
    form.productImage.data = product.productImage
    form.stock.data = product.stockLeft
    form.isRecommended.data = product.isRecommended
    form.price.data = product.price

@app.route('/item')
def item():
    return render_template('item.html', items=Item.query.all())

@app.route('/category')
def category():
    return render_template('category.html', categories=Category.query.all())

@app.route('/cart')
def cart():
    return render_template('cart.html', carts=Cart.query.all())

@app.route('/cart/<cart_cartID>')
def cart_id(cart_cartID):
    curr_cart = Cart.query.filter(Cart.cartID == cart_cartID).one()
    curr_buyer = User.query.filter(User.id == curr_cart.buyerID).one()
    return render_template('cart-item.html',
        curr_cart = curr_cart, curr_buyer = curr_buyer,
        items = IsPlacedInCart.query.filter(IsPlacedInCart.cartID == cart_cartID))

@app.route('/order')
def order():
    return render_template('order.html', orders=Order.query.all())

@app.route('/reviews')
def reviews():
	return render_template('reviews.html', reviews=Reviews.query.all())    

@app.route('/add-reviews', methods=['GET', 'POST'])
def addReviews():
    form = AddReviewsForm()
    if request.method=='POST': # need to validate form
        reviews = Reviews(form.reviewsID.data, form.rating.data, form.commentary.data, form.dateReviewed.data, form.userID.data, form.modelNum.data)
        save_reviews_add(reviews, form, new=True)        
        flash(f'You successfully created a review with rating {form.rating.data}! Thanks for your feedback.', 'success')
        return redirect(url_for('reviews')) # redirect to product page so they can see the updated table
    return render_template('add-reviews.html', title='Create a review for your product', form=form)

def save_reviews_add(reviews, form, new=False):
    """
    Save adding the reviews to the database
    """
    # Get data from form and assign it to the correct attributes of the SQLAlchemy table object

    # data from the user input
    reviews.reviewsID = form.reviewsID.data
    reviews.rating = form.rating.data
    reviews.commentary = form.commentary.data
    reviews.dateReviewed = form.dateReviewed.data 
    reviews.userID = form.userID.data
    reviews.modelNum = form.modelNum.data
    if new:
        db.session.add(reviews)
    db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if request.method == 'POST':
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main'))
        else: 
            flash('Login unsuccessful. Check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/choose-registration')
def chooseRegistration():
    return render_template('choose-user-type.html')

@app.route('/register/<type>', methods=['GET', 'POST'])
def register(type):
    form = AddBuyerForm()
    if type == 'seller':
        form = AddSellerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password,
            type=type, dateJoined=datetime.date(datetime.now()))
        db.session.add(user)
        db.session.commit()

        if type == 'buyer':
            buyer = Buyer(buyerID=user.get_id(), balance=form.balance.data, 
                shippingAddress=form.shippingAddress.data, billingAddress=form.billingAddress.data,
                photo=form.photo.data, name=form.name.data, email=form.email.data)
            db.session.add(buyer)
            db.session.commit()
        else:
            seller = Seller(sellerID=user.get_id(), name=form.name.data, email=form.email.data)
            db.session.add(seller)
            db.session.commit()

        create_user_cart(user.get_id(), type, new=True)
        flash(f'You successfully created a {type} account!', 'success')
        return redirect(url_for('login')) 
    return render_template('add-user.html', title='Create an account', form=form, user_type=type)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()