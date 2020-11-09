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
    for line in range(10): # for now, just test with a really small amount of data
        raw_sellers = data.iloc[line]['sellers']
        if raw_sellers == raw_sellers: # will only work with rows that have sellers
            process_seller_row(data, line)
            count += 1
        else:
            continue
    print(count)

    buyer_info = {}
    newcount = 0
    for i in range(10):
        raw_review_info = data.iloc[i]['customer_reviews']
        if raw_review_info == raw_review_info:
            get_all_buyerinfo(i, raw_review_info, buyer_info)
            process_single_buyer(buyer_info[i], newcount)
            newcount += 1
        else:
            continue
    # after all the rows are processed, add the categories
    seed_category_info()
    print(newcount)

def get_all_buyerinfo(i, raw_review_info, buyer_info):
    on = 0
    review_info = raw_review_info.strip().split("//")
    misc = review_info[3].split()
    for idx in range(len(misc)):
        if misc[idx]=='on':
            on = idx
    reviewer_name = ' '.join(misc[1:on])
    buyer_info[i]=[reviewer_name]
    return buyer_info

def process_single_buyer(buyer_name, newcount):
    print('---- new buyer ----')
    newbuyer = buyer_name[0]
    print(newbuyer)
    # create user because user needs to exist before seller
    encryptedPassword = bcrypt.generate_password_hash("password").decode('utf-8')
    buyerEmail = newbuyer+"@gmail.com"
    existingUser = User.query.filter(User.email == buyerEmail).first()
    if existingUser is None:
        user = User(newbuyer, buyerEmail, encryptedPassword, "buyer", datetime.date(datetime.now()), "Elementary School")
        db.session.add(user)
        db.session.commit()
        # create buyer
        buyer = Buyer(user.get_id(), 150.00, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "/static/images/blankprofilepic.png", newbuyer, newbuyer+"@gmail.com")
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
            seller_name = value
        if ('Seller_price' in attr):
            seller_price = value
    print(seller_name)
    print(seller_price)
    # create user because user needs to exist before seller
    encryptedPassword = bcrypt.generate_password_hash("password").decode('utf-8')
    # check if user exists
    userEmail = seller_name+"@gmail.com"
    user = User.query.filter(User.email == userEmail).first()
    if user is None:
        user = User(seller_name, seller_name+"@gmail.com", encryptedPassword, "seller", datetime.date(datetime.now()), "Elementary School")
        db.session.add(user)
        db.session.commit()
        # create seller
        seller = Seller(user.get_id(), seller_name, seller_name+"@gmail.com")
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
        print(product_description)
        # product_description = unicodedata2.normalize("NFKD", product_des)
        product_name = data.iloc[line]['product_name'].strip()
        category = data.iloc[line]['amazon_category_and_sub_category'].strip()
        if category!='':
            c_list = category.split('> ')
            c_last = c_list[-1]
            product_img = c_last.replace(' ', '')
            product_image = product_img + '.jpg'
        else:
            product_image = 'Toys.jpg' # default image if category is empty
        stock = (str(data.iloc[line]['number_available_in_stock'])).split('\xa0new')
        # if (stock[0] != stock[0]):
        # if (pd.isna(stock[0])): 
        if (stock[0] == 'nan'): # if nan (it's a string), set stock_left=0
            stock_left = 0
        else:
            stock_left = int(stock[0])
        for num in range(stock_left):
            # create items
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
    # modelNum ('uniq_id'), userID ('seller_name_x'), productDescription ('product_description' + 'product_info'), 
    # productName ('product_name'), productImage (PLACEHOLDER for now)
    # stockLeft ('number_available_in_stock'), isRecommended (yes if 'average_review_rating' is >= 4.0)
    product_count = 0
    model_number = data.iloc[line]['uniq_id'].strip()
    raw_description = str(data.iloc[line]['product_description'])
    raw_info = str(data.iloc[line]['product_information'])
    product_description = (raw_description + '\n \n' + raw_info)
    # product_description = unicodedata2.normalize("NFKD", product_des)
    product_name = data.iloc[line]['product_name'].strip()
    category = data.iloc[line]['amazon_category_and_sub_category'].strip()
    if category!='':
        c_list = category.split('> ')
        c_last = c_list[-1]
        product_img = c_last.replace(' ', '')
        product_image = product_img + '.jpg'
    else:
        product_image = 'Toys.jpg' # default image if category is empty
    stock = (str(data.iloc[line]['number_available_in_stock'])).split('\xa0new')
    # if (stock[0] != stock[0]):
    # if (pd.isna(stock[0])): 
    if (stock[0] == 'nan'): # if nan (it's a string), set stock_left=0
        stock_left = 0
    else:
        stock_left = int(stock[0])
    for num in range(stock_left):
        # create items
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
    product = Product(model_number, user.get_id(), product_description, product_name, product_image, 
    stock_left, is_recommended, price)
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


def get_all_reviewinfo(csv):
    data = pd.read_csv(csv)
    all_review_info = {}
    count = 0
    for i in range(len((data['customer_reviews']))):
        count += 1
        raw_review_info = data.iloc[i]['customer_reviews']
        modelNum = data.iloc[i]['uniq_id']
        if raw_review_info == raw_review_info:
            separate_reviews = raw_review_info.strip().split("|") #finding each separate review for each product, then decomposing each specific review
            for rev in separate_reviews:
                review_info = rev.split(" // ")
                if len(review_info) > 2: #some reviews for a product are incomplete, so we will skip them. for example, product in row 1704 has an
                    headline = review_info[0].strip()
                    #checking if commentary exists; if it doesn't just inserting nothing for commentary
                    try:
                        commentary = review_info[4].strip()
                    except IndexError:
                        commentary = ""
                    date = review_info[2].strip()#getting date
                    misc = review_info[3].split()
                    user_rating = float(review_info[1].strip())

                    for idx in range(len(misc)):#finding where in the string the name is, it's right before on
                        if misc[idx]=='on':
                            on = idx
                    reviewer_name = ' '.join(misc[1:on])

                    if i not in all_review_info: #if a dict entry does not already exist for a product
                        all_review_info[modelNum]=[[user_rating, headline, commentary, date, reviewer_name, modelNum]]
                    else:
                        all_review_info[modelNum].append([user_rating, headline, commentary, date, reviewer_name, modelNum])
        else:
            all_review_info[modelNum]=None #keys of dictioniaries are just the row number
    return all_review_info

#all_ratings = print(len(get_all_ratings('amazon_co-ecommerce_sample.csv')))
#all_numberofreviews = print(len(get_all_numberofreviews('amazon_co-ecommerce_sample.csv')))
#get_all_reviewinfo = print(len(get_all_reviewinfo('amazon_co-ecommerce_sample.csv')))

clean_data('amazon_co-ecommerce_sample.csv')