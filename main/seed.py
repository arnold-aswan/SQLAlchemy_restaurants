from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Customer, Restaurant, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurants.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    fake = Faker()
    
    restaurants = []
    for i in range(10):
        restaurant = Restaurant(
            name = fake.catch_phrase(),
            price = random.randint(100,450),
        )
        
        session.add(restaurant)
        session.commit()
        restaurants.append(restaurant)
        
    customers = []
    for i in range(15):
        customer = Customer(
            first_name = fake.name(),
            last_name = fake.name(),
        )    
        
        session.add(customer)
        session.commit()
        customers.append(customer)
        
    reviews = []
    for customer in customers: #=> iterate throught customers list
        for i in range(random.randint(1,5)): 
            restaurant = random.choice(restaurants)
            if customer not in restaurant.customers:
                restaurant.customers.append(customer)
                session.add(restaurant)
                session.commit()
                
            review = Review(
                rating = random.randint(1,10),
                restaurant_id = restaurant.id,
                customer_id = customer.id,
            )    
            
            reviews.append(review)
            
    session.bulk_save_objects(reviews)        
    session.commit()
    session.close()
    print("done")
        