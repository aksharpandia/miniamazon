from app import db, bcrypt
from models import *
from datetime import date

db.drop_all()
db.create_all()

# adding to user table
encryptedPassword = bcrypt.generate_password_hash("password").decode('utf-8')

user1 = User("jessica", "jessica.su@duke.edu", encryptedPassword, "seller", "10-10-2020")
db.session.add(user1)
user2 = User("kassen", "kassen.qian@duke.edu", encryptedPassword, "seller", "10-11-2020")
db.session.add(user2)
user3 = User("aayush", "aayush.goradia@duke.edu", encryptedPassword, "seller", "10-12-2020")
db.session.add(user3)
user4 = User("nathan", "nathan.parikh@duke.edu", encryptedPassword, "buyer", "10-13-2020")
db.session.add(user4)
user5 = User("akshar", "akshar.pandia@duke.edu", encryptedPassword, "buyer", "10-14-2020")
db.session.add(user5)
user6 = User("another buyer", "another.buyer@duke.edu", encryptedPassword, "buyer", "10-15-2020")
db.session.add(user6)
db.session.commit()

# adding to seller table - make sure these users exist first
seller0 = Seller(1, "jessica", "jessica.su@duke.edu")
db.session.add(seller0)
seller1 = Seller(2, "kassen", "kassen.qian@duke.edu")
db.session.add(seller1)
seller2 = Seller(3, "aayush", "aayush.goradia@duke.edu")
db.session.add(seller2)

db.session.commit()

# adding to buyer table - make sure these users exist first
buyer0 = Buyer(4, 200.01, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "/static/images/nathan.png", "nathan", "nathan.parikh@duke.edu")
db.session.add(buyer0)
buyer1 = Buyer(5, 200.01, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "/static/images/blankprofilepic.png", "akshar", "akshar.pandia@duke.edu")
db.session.add(buyer1)
buyer2 = Buyer(6, 200.01, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "/static/images/blankprofilepic.png", "another buyer", "another.buyer@duke.edu")
db.session.add(buyer2)

db.session.commit()

# adding to product table (10 products) - make sure all the userID match IDs int he SELLER table
product1 = Product(123456789, 1, '13-inch MacBook Pro', '13MacBookPro.jpeg', '13" MacBook Pro', 4, True, 1200.00)
db.session.add(product1)
product2 = Product(123456790, 1, '16-inch MacBook Pro', 'img2.jpg', '16" MacBook Pro', 2, False, 1500.00)
db.session.add(product2)
product3 = Product(123456791, 1, '11-inch MacBook Air', 'img6.jpg', '11" MacBook Air', 2, False, 1100.00)
db.session.add(product3)
product4 = Product(123456792, 1, '13-inch MacBook Air', 'img7.jpg', '13" MacBook Air', 2, True, 1255.00)
db.session.add(product4)
product5 = Product(246468680, 2, 'iPhone 11 w/ 64GB of storage', 'img3.jpg', '64GB iPhone 11', 4, False, 900.00)
db.session.add(product5)
product6 = Product(246468681, 2, 'iPhone 11 w/ 128GB of storage', 'img4.jpg', '128GB iPhone 11', 4, True, 999.99)
db.session.add(product6)
product7 = Product(246468682, 2, 'iPhone 11 w/ 256GB of storage', 'img5.jpg', '256GB iPhone 11', 4, True, 1099.99)
db.session.add(product7)
product8 = Product(135357579, 3, '12.9-inch iPad Pro (4th generation)', 'img8.jpg', 'iPad Pro 4th Generation', 4, True, 800.00)
db.session.add(product8)
product9 = Product(135357580, 3, '10.9-inch iPad Air (4th generation)', 'img9.jpg', 'iPad Air 4th Generation', 2, False, 700.00)
db.session.add(product9)
product10 = Product(135357581, 3, '10.2-inch iPad (8th generation)', 'img10.jpg', 'iPad 8th Generation', 2, False, 600.00)
db.session.add(product10)

db.session.commit()

# adding to item table (10 items)
item1 = Item(123000001, True, 123456789, 1)
db.session.add(item1)
item2 = Item(123000002, True, 123456789, 1) 
db.session.add(item2)
item3 = Item(123000003, True, 123456790, 1) 
db.session.add(item3)
item4 = Item(123000004, True, 123456791, 1) 
db.session.add(item4)
item5 = Item (246000001, True, 123456792, 1,) 
db.session.add(item5)
item6 = Item (246000002, True, 246468680, 2,) 
db.session.add(item6)
item7 = Item (246000003, True, 246468680, 2,) 
db.session.add(item7)
item8 = Item (135000001, True, 246468681, 2,) 
db.session.add(item8)
item9 = Item (135000002, True, 246468681, 2) 
db.session.add(item9)
item10 = Item (135000003, False, 246468682, 2) 
db.session.add(item10)

item11 = Item(357000001, True, 246468682, 2) 
db.session.add(item11)
item12 = Item(357000002, False, 246468682, 2) 
db.session.add(item12)
item13 = Item(357000003, False, 135357579, 3) 
db.session.add(item13)
item14 = Item(357000004, False, 135357579, 3) 
db.session.add(item14)
item15 = Item (579000001, True, 135357579, 3) 
db.session.add(item15)
item16 = Item (579000002, True, 135357579, 3) 
db.session.add(item16)
item17 = Item (579000003, False, 135357580, 3) 
db.session.add(item17)
item18 = Item (791000001, True, 135357580, 3) 
db.session.add(item18)
item19 = Item (791000002, False, 135357581, 3) 
db.session.add(item19)
item20 = Item (791000003, False, 135357581, 3) 
db.session.add(item20)

item21 = Item(123000005, False, 123456789, 1)
db.session.add(item21)
item22 = Item(123000006, False, 123456789, 1) 
db.session.add(item22)
item23 = Item(123000007, False, 123456790, 1) 
db.session.add(item23)
item24 = Item(123000008, False, 123456791, 1) 
db.session.add(item24)
item25 = Item (123000009, False, 123456792, 1,) 
db.session.add(item25)
item26 = Item (246000004, False, 246468680, 2,) 
db.session.add(item26)
item27 = Item (246000005, False, 246468680, 2,) 
db.session.add(item27)
item28 = Item (246000006, False, 246468681, 2,) 
db.session.add(item28)
item29 = Item (246000007, False, 246468681, 2) 
db.session.add(item29)
item30 = Item (246000008, False, 246468682, 2) 
db.session.add(item30)

db.session.commit()

# adding to category table (2 categories)
category1 = Category('Electronics', 10)
db.session.add(category1)
category2 = Category('Books', 0)
db.session.add(category2)
db.session.commit()

#adding to BelongsToCategory table
belongs1 = BelongsToCategory(123456789, 'Electronics')
db.session.add(belongs1)
belongs2 = BelongsToCategory(123456790, 'Electronics')
db.session.add(belongs2)
belongs3 = BelongsToCategory(123456791, 'Electronics')
db.session.add(belongs3)
belongs4 = BelongsToCategory(123456792, 'Electronics')
db.session.add(belongs4)
belongs5 = BelongsToCategory(246468680, 'Electronics')
db.session.add(belongs5)
belongs6 = BelongsToCategory(246468681, 'Electronics')
db.session.add(belongs6)
belongs7 = BelongsToCategory(246468682, 'Electronics')
db.session.add(belongs7)
belongs8 = BelongsToCategory(135357579, 'Electronics')
db.session.add(belongs8)
belongs9 = BelongsToCategory(135357580, 'Electronics')
db.session.add(belongs9)
belongs10 = BelongsToCategory(135357581, 'Electronics')
db.session.add(belongs10)
db.session.commit()

# adding to cart table
cart1 = Cart(444, 4, "2020-10-10")
db.session.add(cart1)
cart2 = Cart(555, 5, "2020-10-02")
db.session.add(cart2)
cart3 = Cart(666, 6, "2020-10-11")
db.session.add(cart3)
db.session.commit()


# adding to isPlacedInCart table
itemcart1 = IsPlacedInCart(444, 357000002)
db.session.add(itemcart1)
# itemcart2 = IsPlacedInCart(444, 357000003)
# db.session.add(itemcart2)
# itemcart3 = IsPlacedInCart(444, 579000003)
# db.session.add(itemcart3)
# itemcart4 = IsPlacedInCart(555, 791000002)
# db.session.add(itemcart4)
# itemcart5 = IsPlacedInCart(666, 791000003)
# db.session.add(itemcart5)
db.session.commit()


# adding to order table
order1 = Order(1000, 4, 3900.00, "express", "10-01-2020")
db.session.add(order1)
order2 = Order(1001, 4, 1100.00, "5-day", "10-02-2020")
db.session.add(order2)
order = Order(1002, 4, 1255.00, "express", "10-02-2020")
db.session.add(order)
order = Order(1003, 5, 1255.00, "express", "10-03-2020")
db.session.add(order)
order = Order(1004, 5, 900.00, "prime", "10-03-2020")
db.session.add(order)
order = Order(1005, 5, 900.00, "10-day", "10-04-2020")
db.session.add(order)
order = Order(1006, 4, 999.99, "express", "10-04-2020")
db.session.add(order)
order = Order(1007, 6, 2899.98, "express", "10-05-2020")
db.session.add(order)
order = Order(1008, 4, 800.00, "express", "10-05-2020")
db.session.add(order)
order = Order(1009, 5, 700.00, "express", "10-05-2020")
db.session.add(order)
db.session.commit()
# Commenting out orders for simplicity with testing
# order = Order(1010, 5, 1.00, "prime", "10-06-2020")
# db.session.add(order)
# order = Order(1011, 5, 0.22, "10-day", "10-07-2020")
# db.session.add(order)
# order = Order(1012, 6, 1.76, "express", "10-09-2020")
# db.session.add(order)
# order = Order(1013, 4, 100.98, "express", "10-09-2020")
# db.session.add(order)
# order = Order(1014, 5, 0.22, "10-day", "10-10-2020")
# db.session.add(order)
# order = Order(1015, 6, 1.76, "5-day", "10-10-2020")
# db.session.add(order)
# order = Order(1016, 4, 100.98, "express", "10-10-2020")
# db.session.add(order)
# order = Order(1017, 4, 22.33, "5-day", "10-11-2020")
# db.session.add(order)
# order = Order(1018, 5, 12.3, "express", "10-11-2020")
# db.session.add(order)
# order = Order(1019, 5, 9.09, "10-day", "10-11-2020")
# db.session.add(order)
# order = Order(1020, 6, 89.99, "express", "10-13-2020")
# db.session.add(order)
# order = Order(1021, 6, 92.32, "express", "10-16-2020")
# db.session.add(order)

# *NEW* ItemsinOrder Relationship Set
itemtoadd = ItemsInOrder(1000, 123000001)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1000, 123000002)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1000, 123000003)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1001, 123000004)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1002, 246000001)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1003, 246000001)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1004, 246000002)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1005, 246000003)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1006, 135000001)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1007, 135000002)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1007, 357000001)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1007, 579000001)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1008, 579000002)
db.session.add(itemtoadd)
itemtoadd = ItemsInOrder(1009, 791000001)
db.session.add(itemtoadd)
db.session.commit()

# adding to review table
reviews1 = Reviews(1, 2, "ok", "awful product", "2020-04-23", 4, 246468680)
db.session.add(reviews1)
reviews2 = Reviews(2, 4, "ok", "decent product", "2020-04-23", 4, 246468680)
db.session.add(reviews2)
reviews3 = Reviews(3, 5, "ok", "a+", "2020-04-23", 5, 246468680)
db.session.add(reviews3)
reviews4 = Reviews(4, 1, "nah", "ok", "2020-04-23", 6, 246468680)
db.session.add(reviews4)
reviews5 = Reviews(5, 1, "ok", "good", "2020-04-23", 4, 246468680)
db.session.add(reviews5)
reviews6 = Reviews(6, 2, "a", "awful product", "2020-04-23", 4, 246468680)
db.session.add(reviews6)
db.session.commit()
# reviews2 = Reviews(2, 3, "decent product", "2020-04-28")
# db.session.add(reviews2)
# reviews3 = Reviews(3, 4, "a+", "2020-03-28")
# db.session.add(reviews3)
# reviews4 = Reviews(4, 4, "ok", "2020-03-28")
# db.session.add(reviews4)
# reviews5 = Reviews(5, 4, "decent", "2020-03-28")
# db.session.add(reviews5)
# reviews6 = Reviews(6, 4, "nice", "2020-03-28")
# db.session.add(reviews6)
# reviews7 = Reviews(7, 4, "ok", "2020-03-28")
# db.session.add(reviews7)
# reviews8 = Reviews(8, 4, "ok", "2020-03-28")
# db.session.add(reviews8)
# reviews9 = Reviews(9, 4, "ok", "2020-03-28")
# db.session.add(reviews9)
# reviews10 = Reviews(10, 4, "ok", "2020-03-28")
# db.session.add(reviews10)

db.session.commit()
