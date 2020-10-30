from app import db
from models import *
from datetime import date

db.drop_all()
db.create_all()

# adding to user table
user1 = User(0, "jessica", "jessica.su@duke.edu", "password", "seller", "10-10-2020", 200.01, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "jessicapic.jpg")
db.session.add(user1)
user2 = User(1, "kassen", "kassen.qian@duke.edu", "password", "seller", "10-11-2020", 200.02, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "kassenpic.jpg")
db.session.add(user2)
user3 = User(2, "aayush", "aayush.goradia@duke.edu", "password", "seller", "10-12-2020", 200.03, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "aayushpic.jpg")
db.session.add(user3)
user4 = User(3, "nathan", "nathan.parikh@duke.edu", "password", "buyer", "10-13-2020", 200.04, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "nathanpic.jpg")
db.session.add(user4)
user5 = User(4, "akshar", "akshar.pandia@duke.edu", "password", "buyer", "10-14-2020", 200.05, "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "aksharpic.jpg")
db.session.add(user5)
user6 = User(5, "another buyer", "another.buyer@duke.edu", "password", "buyer", "10-15-2020", 200.06,
             "300 Research Dr, Durham, NC 27710", "300 Research Dr, Durham, NC 27710", "anotherbuyer.jpg")
db.session.add(user6)

db.session.commit()

# adding to seller table - make sure these users exist first
seller0 = Seller(0)
db.session.add(seller0)
seller1 = Seller(1)
db.session.add(seller1)
seller2 = Seller(2)
db.session.add(seller2)

db.session.commit()

# adding to buyer table - make sure these users exist first
buyer0 = Buyer(3)
db.session.add(buyer0)
buyer1 = Buyer(4)
db.session.add(buyer1)
buyer2 = Buyer(5)
db.session.add(buyer2)

db.session.commit()

# adding to product table (10 products) - make sure all the userID match IDs int he SELLER table
product1 = Product(123456789, 0, '13-inch MacBook Pro', 'img1.jpg', '13" MacBook Pro', 0, True, 1200.00)
db.session.add(product1)
product11 = Product(123456789, 1, '13-inch MacBook Pro', 'img1.jpg', '13" MacBook Pro', 0, True, 900.00)
db.session.add(product11)
product2 = Product(123456790, 0, '16-inch MacBook Pro', 'img2.jpg', '16" MacBook Pro', 1, False, 1200.00)
db.session.add(product2)
product3 = Product(123456791, 0, '11-inch MacBook Air', 'img6.jpg', '11" MacBook Air', 1, False, 1200.00)
db.session.add(product3)
product4 = Product(123456792, 0, '13-inch MacBook Air', 'img7.jpg', '13" MacBook Air', 1, True, 1200.00)
db.session.add(product4)
product5 = Product(246468680, 1, 'iPhone 11 w/ 64GB of storage', 'img3.jpg', '64GB iPhone 11', 1, False, 900.00)
db.session.add(product5)
product6 = Product(246468681, 1, 'iPhone 11 w/ 128GB of storage', 'img4.jpg', '128GB iPhone 11', 1, True, 900.00)
db.session.add(product6)
product7 = Product(246468682, 1, 'iPhone 11 w/ 256GB of storage', 'img5.jpg', '256GB iPhone 11', 1, True, 900.00)
db.session.add(product7)
product8 = Product(135357579, 2, '12.9-inch iPad Pro (4th generation)', 'img8.jpg', 'iPad Pro 4th Generation', 1, True, 800.00)
db.session.add(product8)
product9 = Product(135357580, 2, '10.9-inch iPad Air (4th generation)', 'img9.jpg', 'iPad Air 4th Generation', 1, False, 800.00)
db.session.add(product9)
product10 = Product(135357581, 2, '10.2-inch iPad (8th generation)', 'img10.jpg', 'iPad 8th Generation', 1, False, 700.00)
db.session.add(product10)

db.session.commit()

# adding to item table (10 items)
item1 = Item(123000001, True) 
db.session.add(item1)
item2 = Item(123000002, False) 
db.session.add(item2)
item3 = Item(123000003, False) 
db.session.add(item3)
item4 = Item(123000004, False) 
db.session.add(item4)
item5 = Item (246000001, False) 
db.session.add(item5)
item6 = Item (246000002, False) 
db.session.add(item6)
item7 = Item (246000003, False) 
db.session.add(item7)
item8 = Item (135000001, False) 
db.session.add(item8)
item9 = Item (135000002, False) 
db.session.add(item9)
item10 = Item (135000003, False) 
db.session.add(item10)

item11 = Item(357000001, True) 
db.session.add(item11)
item12 = Item(357000002, False) 
db.session.add(item12)
item13 = Item(357000003, False) 
db.session.add(item13)
item14 = Item(357000004, False) 
db.session.add(item14)
item15 = Item (579000001, False) 
db.session.add(item15)
item16 = Item (579000002, False) 
db.session.add(item16)
item17 = Item (579000003, False) 
db.session.add(item17)
item18 = Item (791000001, False) 
db.session.add(item18)
item19 = Item (791000002, False) 
db.session.add(item19)
item20 = Item (791000003, False) 
db.session.add(item20)

db.session.commit()

# adding to category table (2 categories)
category1 = Category('Electronics', 10)
db.session.add(category1)
category2 = Category('Books', 0)
db.session.add(category2)

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

# adding to cart table
cart1 = Cart(333, 3, "2020-10-10")
db.session.add(cart1)
cart2 = Cart(444, 4, "2020-10-02")
db.session.add(cart2)
cart3 = Cart(555, 5, "2020-10-11")
db.session.add(cart3)

# adding to isPlacedInCart table
itemcart1 = IsPlacedInCart(333, 123000001)
db.session.add(itemcart1)
itemcart2 = IsPlacedInCart(333, 357000001)
db.session.add(itemcart2)
itemcart3 = IsPlacedInCart(333, 579000003)
db.session.add(itemcart3)
itemcart4 = IsPlacedInCart(333, 791000002)
db.session.add(itemcart4)
itemcart5 = IsPlacedInCart(333, 791000003)
db.session.add(itemcart5)


# adding to order table
order1 = Order(1000, 3, 200.21, "express", "10-01-2020")
db.session.add(order1)
order2 = Order(1001, 3, 5.67, "5-day", "10-02-2020")
db.session.add(order2)
order = Order(1002, 3, 2.00, "express", "10-02-2020")
db.session.add(order)
order = Order(1003, 4, 2.00, "express", "10-03-2020")
db.session.add(order)
order = Order(1004, 4, 11, "prime", "10-03-2020")
db.session.add(order)
order = Order(1005, 4, 13.65, "10-day", "10-04-2020")
db.session.add(order)
order = Order(1006, 3, 14.12, "express", "10-04-2020")
db.session.add(order)
order = Order(1007, 5, 21.22, "express", "10-05-2020")
db.session.add(order)
order = Order(1008, 3, 111.2, "express", "10-05-2020")
db.session.add(order)
order = Order(1009, 4, 333.2, "express", "10-05-2020")
db.session.add(order)
order = Order(1010, 4, 1.00, "prime", "10-06-2020")
db.session.add(order)
order = Order(1011, 5, 0.22, "10-day", "10-07-2020")
db.session.add(order)
order = Order(1012, 5, 1.76, "express", "10-09-2020")
db.session.add(order)
order = Order(1013, 3, 100.98, "express", "10-09-2020")
db.session.add(order)
order = Order(1014, 4, 0.22, "10-day", "10-10-2020")
db.session.add(order)
order = Order(1015, 5, 1.76, "5-day", "10-10-2020")
db.session.add(order)
order = Order(1016, 3, 100.98, "express", "10-10-2020")
db.session.add(order)
order = Order(1017, 3, 22.33, "5-day", "10-11-2020")
db.session.add(order)
order = Order(1018, 4, 12.3, "express", "10-11-2020")
db.session.add(order)
order = Order(1019, 4, 9.09, "10-day", "10-11-2020")
db.session.add(order)
order = Order(1020, 5, 89.99, "express", "10-13-2020")
db.session.add(order)

# adding to review table
reviews1 = Reviews(1, 2, "awful product", "2020-04-23", 3, 123456789)
db.session.add(reviews1)
reviews2 = Reviews(2, 4, "decent product", "2020-04-23", 3, 123456789)
db.session.add(reviews2)
reviews3 = Reviews(3, 5, "a+", "2020-04-23", 4, 123456789)
db.session.add(reviews3)
reviews4 = Reviews(4, 1, "ok", "2020-04-23", 5, 123456789)
db.session.add(reviews4)
reviews5 = Reviews(5, 1, "good", "2020-04-23", 3, 123456789)
db.session.add(reviews5)
reviews6 = Reviews(6, 2, "awful product", "2020-04-23", 3, 123456789)
db.session.add(reviews6)
reviews7 = Reviews(7, 3, "ok", "2020-04-23", 3, 123456789)
db.session.add(reviews7)
reviews8 = Reviews(8, 2, "nice", "2020-04-23", 3, 123456789)
db.session.add(reviews8)
reviews9 = Reviews(9, 2, "awful", "2020-04-23", 3, 123456789)
db.session.add(reviews9)
reviews10 = Reviews(10, 2, "ok", "2020-04-23", 3, 123456789)
db.session.add(reviews10)
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
