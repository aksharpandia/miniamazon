from app import db, bcrypt
from models import *
import pandas as pd
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
    for line in range(5): # for now, just test with a really small amount of data
        raw_sellers = data.iloc[line]['sellers']
        if raw_sellers == raw_sellers: # will only work with rows that have sellers
            process_seller_row(data, line)
            count += 1
        else:
            continue
    print(count)

    buyer_info = {}
    newcount = 0
    for i in range(5):
        raw_review_info = data.iloc[i]['customer_reviews']
        if raw_review_info == raw_review_info:
            get_all_buyerinfo(i, raw_review_info, buyer_info)
            process_single_buyer(buyer_info[i], newcount)
            newcount += 1
        else:
            continue
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
    user = User(newbuyer, newbuyer+"@gmail.com", encryptedPassword, "buyer", datetime.date(datetime.now()))
    db.session.add(user)
    db.session.commit()
    # create buyer
    buyer = Buyer(user.get_id(), 150.00, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "/static/images/blankprofilepic.png", newbuyer, newbuyer+"@gmail.com")
    db.session.add(buyer)
    db.session.commit()
    # to do: create cart (since every buyer needs to have a cart)

def process_seller_row(data, line):
    print('---- new product ----')
    string_json_sellers = data.iloc[line]['sellers'].replace('=>', ':')
    json_sellers = json.loads(string_json_sellers)
    has_multiple_sellers = isinstance(json_sellers['seller'], list)
    sellers = json_sellers['seller']
    if has_multiple_sellers:
        for seller in sellers:
            process_single_seller(seller)
    else:
        process_single_seller(sellers)

def process_single_seller(seller):
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
    user = User(seller_name, seller_name+"@gmail.com", encryptedPassword, "seller", datetime.date(datetime.now()))
    db.session.add(user)
    db.session.commit()
    # create seller
    seller = Seller(user.get_id(), seller_name, seller_name+"@gmail.com")
    db.session.add(seller)
    db.session.commit()

    # will need to create product here

clean_data('amazon_co-ecommerce_sample.csv')