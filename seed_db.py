import random
from faker import Faker
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import timedelta

Faker.seed(42)
random.seed(42)
fake = Faker()

Base = declarative_base()
engine = create_engine("sqlite:///ecommerce.db", echo=False)
Session = sessionmaker(bind=engine)


class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    city = Column(String)
    joined_date = Column(DateTime)


class Product(Base):
    __tablename__ = "products"
    product_id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    rating = Column(Float)


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    product_id = Column(String, ForeignKey("products.product_id"))
    status = Column(String)
    order_date = Column(DateTime)
    estimated_delivery = Column(DateTime)
    tracking_number = Column(String)


class Return(Base):
    __tablename__ = "returns"
    return_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.order_id"))
    reason = Column(String)
    status = Column(String)
    refund_amount = Column(Float)
    created_at = Column(DateTime)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = Session()

categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]

# Products - 50 total, first 5 have zero stock
products = []
for i in range(1, 51):
    products.append(Product(
        product_id=f"P{i:04d}",
        name=fake.catch_phrase(),
        category=random.choice(categories),
        price=round(random.uniform(10, 500), 2),
        stock=0 if i <= 5 else random.randint(1, 100),
        rating=round(random.uniform(1.0, 5.0), 1)
    ))
session.add_all(products)

# Customers - 50 total
customers = []
for i in range(1, 51):
    customers.append(Customer(
        customer_id=f"C{i:04d}",
        name=fake.name(),
        email=fake.email(),
        city=fake.city(),
        joined_date=fake.date_time_between(start_date="-2y", end_date="now")
    ))
session.add_all(customers)
session.commit()

# Orders - 100 total, first 10 customers get multiple orders
statuses = ["processing", "shipped", "delivered", "cancelled"]
orders = []
multi_order_customers = [f"C{i:04d}" for i in range(1, 11)]

for i in range(1, 101):
    if i <= 20:
        cid = multi_order_customers[i % 10]
    else:
        cid = f"C{random.randint(1, 50):04d}"
    pid = f"P{random.randint(1, 50):04d}"
    odate = fake.date_time_between(start_date="-1y", end_date="now")
    orders.append(Order(
        order_id=f"O{i:04d}",
        customer_id=cid,
        product_id=pid,
        status=random.choice(statuses),
        order_date=odate,
        estimated_delivery=odate + timedelta(days=random.randint(3, 14)),
        tracking_number=fake.bothify(text="TRK-#######")
    ))
session.add_all(orders)
session.commit()

# Returns - only from delivered orders
delivered_orders = session.query(Order).filter_by(status="delivered").all()
return_reasons = ["Defective product", "Wrong item delivered", "Changed my mind", "Better price found"]
return_statuses_list = ["pending", "approved", "rejected"]

for i, order in enumerate(delivered_orders[:30], 1):
    session.add(Return(
        return_id=f"R{i:04d}",
        order_id=order.order_id,
        reason=random.choice(return_reasons),
        status=random.choice(return_statuses_list),
        refund_amount=round(random.uniform(10, 300), 2),
        created_at=fake.date_time_between(start_date="-6m", end_date="now")
    ))
session.commit()

print("=" * 40)
print("✅ Database seeded successfully!")
print("=" * 40)
print(f"  Customers : {session.query(Customer).count()}")
print(f"  Products  : {session.query(Product).count()}")
print(f"  Orders    : {session.query(Order).count()}")
print(f"  Returns   : {session.query(Return).count()}")
print("=" * 40)
session.close()