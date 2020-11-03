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