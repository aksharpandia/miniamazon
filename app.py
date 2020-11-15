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


# def join_item_product(cartID):
#     # return IsPlacedInCart.query.join(Item, Item.itemID == IsPlacedInCart.itemID).\
#     #     filter(IsPlacedInCart.cartID == cartID)

#     return db.session.query(IsPlacedInCart).filter(IsPlacedInCart.cartID== cartID).\
#     join(Item, Item.itemID == IsPlacedInCart.itemID).all()

#    # return db.session.query(IsPlacedInCart, Item).filter

#     # db.session.query(Product.productName, Product.modelNum, db.func.count(Item.isSold).label("numSold")).join(Item, Product.modelNum == Item.modelNum)
#     #     .filter(Item.isSold.is_(True), Product.userID == current_user.id).group_by(Product.modelNum, Product.productName).all())
    

@app.route('/search-results', methods=['GET', 'POST'])
def searchResults():
    results = []
    search_string = request.form['search']
    if search_string != '':
        results = Product.query.filter(Product.productName.contains(search_string)) # this is case sensitive
        if results.first()==None:
            flash('No results found!')
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
def buyer_ID():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('specific-buyer.html', 
        curr_buyer=Buyer.query.filter(Buyer.buyerID == current_user.id).first(), orders = Order.query.filter(Order.buyerID==current_user.id).all(), form=form
    )

@app.route('/buyer/addBalance', methods=['GET', 'POST'])
def addBalance():
    form = AddBalanceForm()
    curr_buyer = Buyer.query.filter(Buyer.buyerID == current_user.id).first()
    if request.method == 'POST': # need to validate form
        mynewbalance = form.newbalance.data
        if (isinstance(mynewbalance, float) and mynewbalance>0):
            balance = curr_buyer.balance + mynewbalance
            save_balance_add(curr_buyer, balance, form, new=True)
            flash(f'You added {form.newbalance.data} to the balance', 'success')
            return redirect('/buyer') # redirect to buyer profile page so they can see the updated table
        else:
            flash("Invalid Amount: Try Again!")
            return redirect('/buyer/addBalance')
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
            .with_entities(User.name, Product.stockLeft, Product.price, Product.modelNum, Product.userID),
        # curr_category=BelongsToCategory.query.filter(BelongsToCategory.modelNum == model_num).one(),
        # categories=BelongsToCategory.query.filter(BelongsToCategory.modelNum == model_num),
        ratings=Reviews.query.filter(Reviews.modelNum == model_num),
        avg_rating=str(Reviews.query.filter(Reviews.modelNum == model_num).with_entities(func.avg(Reviews.rating)).one()[0]).rstrip('0'),
        form=form,
        reviews=Reviews.query.filter(Reviews.modelNum == model_num),
        mycart = Cart.query.filter(Cart.buyerID == current_user.id).first()
        )

@app.route('/add-product/<seller_id>', methods=['GET', 'POST'])
def addProduct(seller_id):
    form = AddProductForm()
    if request.method=='POST': # need to validate form
        product = Product(form.productName.data, form.modelNum.data, current_user.id,
                        form.productDescription.data, form.productImage.data, form.stock.data, form.isRecommended.data,
                        form.price.data, form.category.data)
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

@app.route('/delete_product_from_cart/<model_num>/<user_id>/<cart_id>', methods=['GET', 'POST'])
def delete_product_from_cart(model_num, user_id, cart_id):
    itemstodel = db.session.query(IsPlacedInCart).\
        join(Item, Item.itemID == IsPlacedInCart.itemID).\
        filter(Item.modelNum == model_num, Item.userID == user_id).all()
    for itemtodel in itemstodel:
        db.session.delete(itemtodel)
        db.session.commit()
    flash(
        f'You successfully deleted this product (Model Number: ' + model_num + ') from your cart', 'success')
    return redirect('/cart/' + cart_id)

@app.route('/updatecart/<cart_id>/<model_num>/<user_id>', methods=['GET', 'POST'])
def updateCart(cart_id, model_num, user_id):
    if request.method == 'POST':
        # Same item can't be added to different users' carts
        itemsincart = [i.itemID for i in db.session.query(IsPlacedInCart).all()]
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
        total_price = find_price_of_cart(cart_id)
        validBalance, currentBalance = checkBalance(total_price, cart_id)
        if validBalance is False:
            flash(
                f'Your balance of ${currentBalance} is insufficient. Please navigate to Buyer Profile to add more balance.', 'failure')
            return redirect('/cart/' + cart_id)
        orderID = randint(0,999999)
        newOrder = Order(orderID, current_user.id, total_price, 'express', datetime.date(datetime.now()))
        db.session.add(newOrder)
        db.session.commit()
        itemsincart = [i.itemID for i in db.session.query(IsPlacedInCart).\
            filter(IsPlacedInCart.cartID == cart_id).all()]
        productsincart = find_products_in_cart(cart_id)

        for itemID in itemsincart:
            add_item_to_order(orderID, itemID)
            delete_item_from_cart(itemID, cart_id)
            change_isSold_flag(itemID)

        for entry in productsincart:
            change_product_quantity(entry)

        change_buyer_balance(total_price, cart_id)
            
        flash(
            f'You successfully created Order {newOrder.orderID}!', 'success')
        return redirect('/order')

def checkBalance(total_price, cart_id):
    buyer_to_check = db.session.query(Buyer).\
        join(Cart, Cart.buyerID==Buyer.buyerID).filter(Cart.cartID == cart_id).first()
    balance = buyer_to_check.balance
    if balance < total_price:
        return False, balance
    return True, balance

def add_item_to_order(orderID, itemID):
    newItemsInOrder = ItemsInOrder(orderID, itemID)
    db.session.add(newItemsInOrder)
    db.session.commit()

def delete_item_from_cart(itemID, cart_id):
    itemtodel = IsPlacedInCart.query.filter(IsPlacedInCart.itemID == itemID,
        IsPlacedInCart.cartID == cart_id).first()
    db.session.delete(itemtodel)
    db.session.commit()

def change_isSold_flag(itemID):
    for item in db.session.query(Item).filter(Item.itemID == itemID):
        item.isSold = True
        db.session.add(item)
        db.session.commit()

def change_buyer_balance(total_price, cart_id):
    buyer_to_edit = db.session.query(Buyer).\
        join(Cart, Cart.buyerID==Buyer.buyerID).filter(Cart.cartID == cart_id).first()
    buyer_to_edit.balance = round(buyer_to_edit.balance - total_price, 2)
    db.session.add(buyer_to_edit)
    db.session.commit()

def change_product_quantity(entry):
    modelNum = entry[2]
    userID = entry[3]
    quantity = entry[4]
    product_to_edit = db.session.query(Product).filter(Product.modelNum == modelNum,
        Product.userID == userID).first()
    product_to_edit.stockLeft = product_to_edit.stockLeft - quantity
    db.session.add(product_to_edit)
    db.session.commit()

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
    curr_cart = Cart.query.filter(current_user.id == Cart.buyerID).first()
    if request.method == 'POST':
        return searchResults(search)
    return redirect('/cart/' + str(curr_cart.cartID))

@app.route('/cart/<cart_cartID>')
def cart_id(cart_cartID):
    curr_cart = Cart.query.filter(Cart.cartID == cart_cartID).one()
    curr_buyer = User.query.filter(User.id == curr_cart.buyerID).one()

    # Returns on per product basis (Model Number, Product Name, Sold By, Quantity in cart, Price per unit)
    productsincart = find_products_in_cart(cart_cartID)
    total_price = find_price_of_cart(cart_cartID)

    return render_template('cart-item.html',
        curr_cart = curr_cart, curr_buyer = curr_buyer,
        products=productsincart,
        total_price = total_price)

def find_products_in_cart(cartID):
    # Product Name, Model Number, Sold By (user id), Quantity, Price per unit
    return db.session.query(db.func.min(Product.productImage), db.func.min(Product.productName), Item.modelNum,
        Item.userID, db.func.count(IsPlacedInCart.itemID), db.func.min(Product.price)).\
        join(IsPlacedInCart, IsPlacedInCart.itemID == Item.itemID).\
        join(Product, (Item.userID == Product.userID) & (Item.modelNum == Product.modelNum)).\
        filter(IsPlacedInCart.cartID==cartID).\
        group_by(Item.modelNum, Item.userID).all()

def find_price_of_cart(cartID):
    total_price = db.session.query(db.func.sum(Product.price)).\
        join(Item, (Item.modelNum == Product.modelNum) & (Item.userID == Product.userID)).\
        join(IsPlacedInCart, IsPlacedInCart.itemID == Item.itemID).\
        filter(IsPlacedInCart.cartID==cartID).all()
    total_price = total_price[0][0] #some weird SQL thing
    if total_price == None:
        total_price = 0
    return total_price

@app.route('/order')
def order():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('order.html', orders=Order.query.filter(Order.buyerID==current_user.id).all(), form=form)

@app.route('/order/<order_id>')
def order_id(order_id):
    curr_order = Order.query.filter(Order.orderID == order_id).one()
    curr_buyer = User.query.filter(User.id == curr_order.buyerID).one()
    productsinorder = find_products_in_order(order_id)

    return render_template('order-item.html',
        curr_order = curr_order, curr_buyer = curr_buyer,
        products=productsinorder,
        total_price = curr_order.transacAmount)

def find_products_in_order(orderID):
    # Product Name, Model Number, Sold By (user id), Quantity, Price per unit
    return db.session.query(db.func.min(Product.productName), Item.modelNum,
        Item.userID, db.func.count(ItemsInOrder.itemID), db.func.min(Product.price)).\
        join(ItemsInOrder, ItemsInOrder.itemID == Item.itemID).\
        join(Product, (Item.modelNum == Product.modelNum) & (Item.userID == Product.userID)).\
        filter(ItemsInOrder.orderID == orderID).\
        group_by(Item.modelNum, Item.userID).all()


@app.route('/reviews')
def reviews():
    form = SearchForm()
    if request.method == 'POST':
        return searchResults(search)
    return render_template('reviews.html', reviews=Reviews.query.all(), form=form)    

@app.route('/add-reviews/<modelNum>', methods=['GET', 'POST'])
def addReviews(modelNum):
    form = AddReviewsForm()
    if request.method=='POST': # need to validate form
        reviews = Reviews(form.rating.data, form.headline.data, form.commentary.data, datetime.date(datetime.now()), current_user.id, modelNum)
        exists = bool(db.session.query(Product).filter_by(modelNum=modelNum).first()) #checking if model num exists in product table
        if exists: 
            save_reviews_add(reviews, form, modelNum, new=True)  
        else:
            return "Model number does not exist"      
        flash(f'You successfully created a review with rating {form.rating.data}! Thanks for your feedback.', 'success')
        return redirect('/product/'+modelNum)
    return render_template('add-reviews.html', title='Create a review for your product', form=form)

def save_reviews_add(reviews, form, modelNum, new=False):
    """
    Save adding the reviews to the database
    """
    # Get data from form and assign it to the correct attributes of the SQLAlchemy table object

    # data from the user input
    reviews.rating = form.rating.data
    reviews.headline = form.headline.data
    reviews.commentary = form.commentary.data
    reviews.dateReviewed = datetime.date(datetime.now())
    reviews.userID = current_user.id
    reviews.modelNum = modelNum
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
            type=type, dateJoined=datetime.date(datetime.now()), securityQuestionAnswer=form.securityQuestionAnswer.data)
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

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    form = ForgotPasswordForm()
    if request.method=='POST':
        currUser = User.query.filter(User.email == form.email.data).first()
        if currUser.securityQuestionAnswer == form.securityQuestionAnswer.data:
            return redirect(url_for('newPassword', user_id=currUser.id))
        else:
            flash('Could not verify the answer to your security question. Please try again', 'danger')
    return render_template('forgot-password.html', form=form)

@app.route('/new-password/<user_id>', methods=['GET', 'POST'])
def newPassword(user_id):
    form = NewPasswordForm()
    if form.validate_on_submit():
        currUser = User.query.filter(User.id == user_id).first()
        currUser.password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
        db.session.commit()
        flash('You successfully updated your password! Try logging in again', 'success')
        return redirect('/login')
    return render_template('new-password.html', form=form)

if __name__ == '__main__':
    app.run()
