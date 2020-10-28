from app import db

# same as creating table
class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    type = db.Column(db.String(120))
    dateJoined = db.Column(db.String(60))
    balance = db.Column(db.Float)
    shippingAddress = db.Column(db.String(120))
    billingAddress = db.Column(db.String(120))
    photo = db.Column(db.String(120))

    def __init__(self, id, name, email, password, type, dateJoined, balance, shippingAddress, billingAddress, photo):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type
        self.dateJoined = dateJoined
        self.balance = balance
        self.shippingAddress = shippingAddress
        self.billingAddress = billingAddress
        self.photo = photo

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Product(db.Model):
    __tablename__ = "product"

    modelNum = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('seller.sellerID'), primary_key=True) # will have to check that user ID is a seller ID
    productDescription = db.Column(db.String(120)) # text for longer string inputs?
    productImage = db.Column(db.String(120)) # image but image files are stored in file system, this is the path to that
    productName = db.Column(db.String(120), nullable=False)
    stockLeft = db.Column(db.Integer, nullable=False)
    isRecommended = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, modelNum, userID, productDescription, productImage, productName, stockLeft, isRecommended, price):
        self.modelNum = modelNum
        self.userID = userID
        self.productDescription = productDescription
        self.productImage = productImage
        self.productName = productName
        self.stockLeft = stockLeft
        self.isRecommended = isRecommended
        self.price = price
    
    def __repr__(self):
        return f"Product('{self.modelNum}', '{self.userID}')"

class Item(db.Model):
    __tablename__ = "item"

    itemID = db.Column(db.Integer, primary_key=True)
    isSold = db.Column(db.Boolean, nullable=False)

    def __init__(self, itemID, isSold):
        self.itemID = itemID 
        self.isSold = isSold 

    def __repr__(self):
        return f"Item('{self.itemID}', '{self.isSold}')"

class Category(db.Model):
    __tablename__ = "category"

    category = db.Column(db.String(60), primary_key=True)
    numberOfItems = db.Column(db.Integer, nullable=False)

    def __init__(self, category, numberOfItems):
        self.category = category 
        self.numberOfItems = numberOfItems 

    def __repr__(self):
        return f"Category('{self.category}', '{self.numberOfItems}')"

class BelongsToCategory(db.Model):
    # relationship set between a product and category
    __tablename__ = "belongstocategory"

    modelNum = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(60), primary_key=True)

    def __init__(self, modelNum, categoryName):
        self.modelNum = modelNum 
        self.categoryName = categoryName 

    def __repr__(self):
        return f"BelongsToCategory('{self.modelNum}', '{self.categoryName}')"

class BelongsToProduct(db.Model):
    # relationship set between an item and a product
    __tablename__ = "belongstoproduct"

    modelNum = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, primary_key=True)

    def __init__(self, modelNum, categoryName):
        self.modelNum = modelNum 
        self.itemID = itemID 

    def __repr__(self):
        return f"BelongsToProduct('{self.modelNum}', '{self.itemID}')"

class Cart(db.Model):
    __tablename__ = "cart"

    cartID = db.Column(db.Integer, primary_key=True)
    buyerID = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    modDateTime = db.Column(db.String(60)) # YYYY-MM-DD

    def __init__(self, cartID, buyerID, modDateTime):
        self.cartID = cartID 
        self.buyerID = buyerID
        self.modDateTime = modDateTime

    def __repr__(self):
        return f"Cart('{self.cartID}'. '{self.buyerID}','{self.modDateTime}')"

class IsPlacedInCart(db.Model):
    __tablename__ = "IsPlacedInCart"

    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'), primary_key=True)
    cartID = db.Column(db.Integer)
    
    def __init__(self, cartID, itemID):
        self.cartID = cartID 
        self.itemID = itemID

    def __repr__(self):
        return f"Cart('{self.cartID}'. '{self.itemID}')"

class Order(db.Model):
    __tablename__ = "order"

    orderID = db.Column(db.Integer, primary_key=True)
    buyerID = db.Column(db.Integer, db.ForeignKey('user.id'))
    transacAmount = db.Column(db.Float, nullable=False)
    deliveryOption = db.Column(db.String(60))
    createdDateTime = db.Column(db.String(60))

    def __init__(self, orderID, buyerID, transacAmount, deliveryOption, createdDateTime):
        self.orderID = orderID
        self.buyerID = buyerID
        self.transacAmount = transacAmount
        self.deliveryOption = deliveryOption
        self.createdDateTime = createdDateTime

    def __repr__(self):
        return f"Order('{self.orderID}','{self.transacAmount}')"

class Reviews(db.Model):
    __tablename__ = "Reviews"
    reviewsID=db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    commentary = db.Column(db.String(120))
    dateReviewed = db.Column(db.String(60))
    userID= db.Column(db.Integer, db.ForeignKey('buyer.buyerID'))
    modelNum = db.Column(db.Integer)
    def __init__(self, reviewsID, rating, commentary, dateReviewed, userID, modelNum):
        self.reviewsID = reviewsID
        self.rating = rating   
        self.commentary = commentary 
        self.dateReviewed = dateReviewed
        self.userID = userID
        self.modelNum = modelNum
    def __repr__(self):
        return f"Reviews('{self.reviewsID}', '{self.rating}', '{self.commentary}', '{self.dateReviewed}', '{self.userID}', '{self.modelNum}')"

class Seller(db.Model):
    __tablename__ = "seller"

    sellerID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)

    def __init__(self, sellerID):
        self.sellerID = sellerID

    def __repr__(self):
        return f"Seller('{self.sellerID}')"

class Buyer(db.Model):
    __tablename__ = "buyer"

    buyerID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)

    def __init__(self, buyerID):
        self.buyerID = buyerID

    def __repr__(self):
        return f"Buyer('{self.buyerID}')"