from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from random import randint
from sqlalchemy.sql import text, func, select
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

@app.route('/', methods=['GET', 'POST'])
@login_required
def main():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(form)
    
    return render_template('index.html',
    curr_product=Product.query.all()[0],
    products=Product.query.all(),
    mycart = Cart.query.filter(Cart.buyerID == current_user.id).first(),
    recommended=Product.query.filter(Product.modelNum==Reviews.modelNum and Reviews.rating >= 4.0).limit(5).all(),
    form=form)

@app.route('/search-results', methods=['GET', 'POST'])
def searchResults():
    results = []
    search_string = request.form['search']
    if search_string != '':
        results = Product.query.filter(Product.productName.contains(search_string)) # this is case sensitive
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('search-results.html', 
            results=results)

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

@app.route('/seller')
def seller_id():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)

    return render_template('seller-product.html', 
        curr_seller=current_user, 
        products=Product.query.filter(Product.userID == current_user.id))

@app.route('/seller-history')
def seller_history():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)

    return render_template('seller-history.html',
    sold_products = db.session.query(Product.productName, Product.modelNum, db.func.count(Item.isSold).label("numSold")).join(Item, Product.modelNum == Item.modelNum)
        .filter(Item.isSold.is_(True), Product.userID == current_user.id).group_by(Product.modelNum, Product.productName).all())

@app.route('/seller-history/<model_num>', methods=['GET', 'POST'])
def seller_history_product(model_num):
    return render_template('seller-history-product.html',
        curr_product = Product.query.filter(Product.modelNum == model_num).first(),
        sold_items = db.session.query(Item.itemID, Buyer.name, Order.createdDateTime).filter(Item.modelNum == model_num).join(ItemsInOrder, Item.itemID == ItemsInOrder.itemID)
        .join(Order, ItemsInOrder.orderID == Order.orderID).join(Buyer, Order.buyerID == Buyer.buyerID))

@app.route('/buyer')
def buyer():
    return render_template('buyer.html', buyers=Buyer.query.all())

@app.route('/buyer/<buyer_ID>')
def buyer_ID(buyer_ID):
    return render_template('specific-buyer.html', 
        curr_buyer=Buyer.query.filter(Buyer.buyerID == buyer_ID).first()
    )

@app.route('/buyer/<buyer_ID>/addBalance', methods=['GET', 'POST'])
def addBalance(buyer_ID):
    form = AddBalanceForm()
    curr_buyer = Buyer.query.filter(Buyer.buyerID == buyer_ID).first()
    if request.method=='POST': # need to validate form
        balance = curr_buyer.balance + form.newbalance.data
        save_balance_add(curr_buyer, balance, form, new=True)
        flash(f'You added {form.newbalance.data} to the balance', 'success')
        return redirect('/buyer/' + str(buyer_ID)) # redirect to buyer profile page so they can see the updated table
    return render_template('add-balance.html', title='Add Balance', form=form)
    

def save_balance_add(curr_buyer, balance, form, new=False):
    curr_buyer.balance = balance
    if new:
        db.session.add(curr_buyer)
    db.session.commit()


@app.route('/product')
def product():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)

    return render_template('product.html', products=Product.query.all(), form=form)

@app.route('/product/<model_num>')
def product_id(model_num):
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)

    return render_template('specific-product.html', 
        curr_product=Product.query.filter(Product.modelNum == model_num).first(),
        products=Product.query.filter(Product.modelNum == model_num),
        # curr_seller=Product.query.filter(Product.modelNum == model_num).with_entities(Product.userID).one(),
        all_sellers=
            Product.query\
            .join(User, User.id == Product.userID).filter(Product.modelNum == model_num)
            .with_entities(User.name, Product.stockLeft, Product.price),
        curr_category=BelongsToCategory.query.filter(BelongsToCategory.modelNum == model_num).one(),
        categories=BelongsToCategory.query.filter(BelongsToCategory.modelNum == model_num),
        ratings=Reviews.query.filter(Reviews.modelNum == model_num),
        avg_rating=str(Reviews.query.filter(Reviews.modelNum == model_num).with_entities(func.avg(Reviews.rating)).one()[0]).rstrip('0'),
        form=form
        )

@app.route('/add-product/<seller_id>', methods=['GET', 'POST'])
def addProduct(seller_id):
    form = AddProductForm()
    if request.method=='POST': # need to validate form
        product = Product(form.productName.data, form.modelNum.data, current_user.id,
                        form.productDescription.data, form.productImage.data, form.stock.data, form.isRecommended.data,
                        form.price.data)
        save_product_add(product, form, new=True)
        flash(f'You added {form.stock.data} {form.productName.data} product(s)!', 'success')
        return redirect('/seller')
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
        return redirect('/seller')


@app.route('/updatecart/<cart_id>/<model_num>/<user_id>', methods=['GET', 'POST'])
def updateCart(cart_id, model_num, user_id):
    if request.method == 'POST':
        itemsincart = [i.itemID for i in db.session.query(IsPlacedInCart).\
            filter(IsPlacedInCart.cartID == cart_id).all()]
        itemtoadd = Item.query.filter(Item.modelNum == model_num, 
            Item.userID == user_id,
            Item.isSold == False,
            ~Item.itemID.in_(itemsincart)).first()
        if itemtoadd is None:
            flash(
            f'Product {model_num} is out of stock!', 'failure')
            return redirect('/cart/' + cart_id)
        reltoadd = IsPlacedInCart(cart_id, itemtoadd.itemID)
        db.session.add(reltoadd)
        db.session.commit()
        flash(
            f'You successfully added {itemtoadd.itemID}!', 'success')
        return redirect('/cart/' + cart_id)

@app.route('/createorder/<cart_id>', methods=['GET', 'POST'])
def createOrder(cart_id):
    if request.method == 'POST':
        orderID = randint(0,999999)
        newOrder = Order(orderID, current_user.id, 100, 'express', "10-01-2020")
        db.session.add(newOrder)
        db.session.commit()
        itemsincart = [i.itemID for i in db.session.query(IsPlacedInCart).\
            filter(IsPlacedInCart.cartID == cart_id).all()]
        for itemID in itemsincart:
            newItemsInOrder = ItemsInOrder(orderID, itemID)
            db.session.add(newItemsInOrder)
            db.session.commit()
            itemtodel = IsPlacedInCart.query.filter(IsPlacedInCart.itemID == itemID,
                IsPlacedInCart.cartID == cart_id).first()
            db.session.delete(itemtodel)
            db.session.commit()
        flash(
            f'You successfully created {newOrder.orderID}!', 'success')
        return redirect('/order')


@app.route('/update_product/<seller_id>/<product_id>',  methods=['GET', 'POST'])
def updateProduct(seller_id, product_id):
    form = AddProductForm()
    prodToUpdate = Product.query.filter(
        Product.modelNum == product_id, Product.userID == seller_id).first()
    
    if request.method == 'POST':
        flash(f'You successfully updated {prodToUpdate.productName}!', 'success')
        save_product_add(prodToUpdate, form, new=False)
        return redirect('/seller')
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
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)

    return render_template('item.html', items=Item.query.all(), form=form)

@app.route('/category')
def category():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('category.html', categories=Category.query.all(), form=form)

@app.route('/cart')
def cart():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('cart.html', carts=Cart.query.all(), form=form)

@app.route('/cart/<cart_cartID>')
def cart_id(cart_cartID):
    curr_cart = Cart.query.filter(Cart.cartID == cart_cartID).one()
    curr_buyer = User.query.filter(User.id == curr_cart.buyerID).one()
    return render_template('cart-item.html',
        curr_cart = curr_cart, curr_buyer = curr_buyer,
        items = IsPlacedInCart.query.filter(IsPlacedInCart.cartID == cart_cartID))

@app.route('/order')
def order():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('order.html', orders=Order.query.all(), form=form)

@app.route('/reviews')
def reviews():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('reviews.html', reviews=Reviews.query.all(), form=form)    

@app.route('/add-reviews', methods=['GET', 'POST'])
def addReviews():
    form = AddReviewsForm()
    if request.method=='POST': # need to validate form
        reviews = Reviews(form.reviewsID.data, form.rating.data, form.headline.data, form.commentary.data, form.dateReviewed.data, form.userID.data, form.modelNum.data)
        exists = bool(db.session.query(Product).filter_by(modelNum=form.modelNum.data).first()) #checking if model num exists in product table
        if exists: 
            save_reviews_add(reviews, form, new=True)  
        else:
            return "Model num does not exist"      
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
    reviews.headline = form.headline.data
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