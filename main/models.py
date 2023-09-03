

from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

restaurant_customers = Table(
    'restaurant_customers',
    Base.metadata,
    Column('restaurant_id', ForeignKey('restaurants.id'), primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), primary_key=True),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())
    
    customers = relationship('Customer', secondary='restaurant_customers', back_populates='restaurants')
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def __repr__(self):
        return f'(Restaurant = {self.restaurant}, ' + \
            f'price= {self.price})'   
    
    def restaurant_reviews(self, restaurant_id):
        reviews = session.query(Review).filter(Review.restaurant_id == restaurant_id).all()
        return [review.rating for review in reviews]
    
    def restaurant_customers(self, restaurant_id):
        customers = session.query(Customer).join(Review).filter(Review.restaurant_id == restaurant_id).all()
        return [customer.first_name for customer in customers]
          
class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String())
    last_name = Column(String())    
    
    restaurants = relationship('Restaurant', secondary='restaurant_customers', back_populates='customers')
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
    def __repr__(self):
        return f'(firstName = {self.first_name}, ' + \
            f'lastName = {self.last_name})'    
            
    def customer_reviews(self, customer_id):
        reviews = session.query(Review).filter(customer_id == Review.customer_id).all()
        return [review.rating for review in reviews]
            
    def customer_restaurants(self, customer_id):
        restaurants = session.query(Restaurant).join(Review).filter(Review.customer_id == customer_id).all()
        return [restaurant.name for restaurant in restaurants]
            
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer(), primary_key=True)
    rating = Column(Integer())
    restaurant_id = Column(Integer(), ForeignKey('restaurants.id'))
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    
    def __init__(self, rating, restaurant_id, customer_id):
        self.rating = rating
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id
    
    def __repr__(self):
        return f'(rating = {self.rating}, ' + \
            f'restaurant_id = {self.restaurant_id}, ' + \
            f'customer_id = {self.customer_id})'
            
    def review_customer(self, review_id):
        customer = session.query(Customer).join(Review).filter(Review.id == review_id).first()
        if customer:
            return f"Customer is {customer.first_name} {customer.last_name}"    
        else:
            return "Customer for the specified id doesn't exist"    
    
    
    def review_restaurant(self, review_id):
        restaurant = session.query(Restaurant).join(Review).filter(Review.id == review_id).first()
        if restaurant:
            return f"Restaurant is {restaurant.name}"
        return f"Restaurant for the specified id doesn't exist"
        
        
        
engine = create_engine('sqlite:///restaurants.db')            
Session = sessionmaker(bind=engine)
session = Session()


# Aggregate and Relationship Methods




# CUSTOMER REVIEWS
# resinstance = Customer('konoha', 'shinden')
# rev = resinstance.customer_reviews(customer_id=3)
# print(rev)

# CUSTOMER REVIEWS
# resinstance = Customer('konoha', 'shinden')
# rev = resinstance.customer_restaurants(customer_id=3)
# print(rev)

# RESTAURANT REVIEWS
# resinstance = Restaurant('konoha',250)
# rev = resinstance.restaurant_reviews(restaurant_id=3)
# print(rev)

# RESTAURANT CUSTOMERS
# resinstance = Restaurant('konoha',250)
# rev = resinstance.restaurant_customers(restaurant_id=3)
# print(rev)


# REVIEW RESTAURANT
# resinstance = Review(3,5,2)
# rev = resinstance.review_restaurant(review_id=2)
# print(rev)

# REVIEW CUSTOMER
# revinstance = Review(5, 3, 2)
# rev = revinstance.review_customer(review_id=2)
# print(rev)

    