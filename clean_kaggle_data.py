from app import db, bcrypt
from models import *
import pandas as pd
import random
import warnings
import json
warnings.simplefilter(action='ignore', category=FutureWarning)
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
from datetime import datetime

# dropping existing databases, then reseeding - once we're ready to get rid of seed_test_db,py, can uncomment these lines
# db.drop_all()
# db.create_all()

def clean_data(csv):
    data = pd.read_csv(csv)
    count = 0
    for line in range(2000): # for now, just test with a really small amount of data
        raw_sellers = data.iloc[line]['sellers']
        if raw_sellers == raw_sellers: # will only work with rows that have sellers
            process_seller_row(data, line)
            count += 1
        else:
            continue
    print(count)

    buyer_info = {}
    newcount = 0
    for i in range(1000):
        raw_review_info = data.iloc[i]['customer_reviews']
        if raw_review_info == raw_review_info:
            separate_reviews = raw_review_info.strip().split("|")
            for rev in separate_reviews:
                review_info = rev.split(" // ")
                get_all_buyerinfo(i, review_info, buyer_info)
                process_single_buyer(buyer_info[i], newcount)
                newcount += 1
        else:
            continue
    # after all the rows are processed, add the categories
    seed_category_info()
    print(newcount)

def get_all_buyerinfo(i, review_info, buyer_info):
    on = 0
    if len(review_info) > 2: #some reviews for a product are incomplete, so we will skip them. for example, product in row 1704 has an
        misc = review_info[3].split()
        for idx in range(len(misc)):
            if misc[idx]=='on':
                on = idx
        reviewer_name = ' '.join(misc[1:on])
        buyer_info[i]=[reviewer_name]
    return buyer_info

def process_single_buyer(buyer_name, newcount):
    print('---- new buyer ----')
    newbuyer = buyer_name[0][:100]
    print(newbuyer)
    # create user because user needs to exist before seller
    encryptedPassword = bcrypt.generate_password_hash("password").decode('utf-8')
    buyerEmail = newbuyer+"@gmail.com"[:100]
    existingUser = User.query.filter(User.email == buyerEmail).first()
    if existingUser is None:
        user = User(newbuyer, buyerEmail, encryptedPassword, "buyer", datetime.date(datetime.now()), "Elementary School")
        db.session.add(user)
        db.session.commit()
        # create buyer
        buyer = Buyer(user.get_id(), 150.00, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "/static/images/blankprofilepic.png", newbuyer, buyerEmail)
        db.session.add(buyer)
        db.session.commit()
    # to do: create cart (since every buyer needs to have a cart)

# global dict for counting categories
categories_dict = {}

def process_seller_row(data, line):
    print('---- new product ----')
    string_json_sellers = data.iloc[line]['sellers'].replace('=>', ':')
    json_sellers = json.loads(string_json_sellers)
    has_multiple_sellers = isinstance(json_sellers['seller'], list)
    sellers = json_sellers['seller']
    if has_multiple_sellers:
        for seller in sellers:
            process_single_seller(seller, data, line)
    else:
        process_single_seller(sellers, data, line)

def process_single_seller(seller, data, line):
    print('---- new seller ----')
    seller_price = 0.00
    seller_name = ''
    for attr, value in seller.items():
        if ('Seller_name' in attr):
            seller_name = value[:100]
        if ('Seller_price' in attr):
            seller_price = value
    print(seller_name)
    print(seller_price)
    # create user because user needs to exist before seller
    encryptedPassword = bcrypt.generate_password_hash("password").decode('utf-8')
    # check if user exists
    userEmail = seller_name+"@gmail.com"[:100]
    user = User.query.filter(User.email == userEmail).first()
    if user is None:
        user = User(seller_name, userEmail, encryptedPassword, "seller", datetime.date(datetime.now()), "Elementary School")
        db.session.add(user)
        db.session.commit()
        # create seller
        seller = Seller(user.get_id(), seller_name, userEmail)
        db.session.add(seller)
        db.session.commit()

        # modelNum ('uniq_id'), userID ('seller_name_x'), productDescription ('product_description' + 'product_info'), 
        # productName ('product_name'), productImage (PLACEHOLDER for now)
        # stockLeft ('number_available_in_stock'), isRecommended (yes if 'average_review_rating' is >= 4.0)
        product_count = 0
        model_number = data.iloc[line]['uniq_id'].strip()
        raw_description = str(data.iloc[line]['product_description'])
        raw_info = str(data.iloc[line]['product_information'])
        product_description = raw_description.replace('Product Description', '')
        product_description = product_description[:100]
        # print(product_description)
        # product_description = unicodedata2.normalize("NFKD", product_des)
        product_name = data.iloc[line]['product_name'].strip()
        product_name = product_name[:100]
        category = data.iloc[line]['amazon_category_and_sub_category']
        if isinstance(category, str):
            c_list = category.split('> ')
            c_last = c_list[-1]
            product_img = c_last.replace(' ', '')
            product_image = product_img + '.jpg'
        else:
            product_image = 'Toys.jpg' # default image if category is empty
            category = 'Hobbies > Model Trains & Railway Sets > Rail Vehicles > Trains' # default category

        stock = (str(data.iloc[line]['number_available_in_stock'])).split('\xa0')
        # if (stock[0] != stock[0]):
        # if (pd.isna(stock[0])): 
        if (stock[0] == 'nan'): # if nan (it's a string), set stock_left=0
            stock_left = 0
        else:
            stock_left = int(stock[0])
        for num in range(stock_left):
            # create items
            item_id = random.randint(0, 1000000)
            while (Item.query.filter(Item.itemID == item_id).first() is not None):
                item_id = random.randint(0, 1000000)
            is_sold = False
            item = Item(item_id, is_sold, model_number, user.get_id())
            db.session.add(item)
            db.session.commit()
        raw_rating = data.iloc[line]['average_review_rating']
        rating = 0.0
        if raw_rating == raw_rating:
            rating = float(raw_rating[0:3]) 
        if (rating >= 4.0):
            is_recommended = True
        else:
            is_recommended = False 
        price = float(seller_price[1:])
        product_count+=1
        # create product 
        product = Product(model_number, user.get_id(), product_description, product_image, product_name, 
        stock_left, is_recommended, price, category)
        db.session.add(product)

        # create category
        if category in categories_dict:
            categories_dict[category] += stock_left
        else:
            categories_dict[category] = 1

def seed_category_info():
    for category, count in categories_dict.items():
        existingCategory = Category.query.filter(Category.category == category).first()
        if existingCategory is None:
            c = Category(category, count)
            db.session.add(c)
            db.session.commit()

clean_data('amazon_co-ecommerce_sample.csv')