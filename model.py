from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import create_engine 
import arrow


db = SQLAlchemy()

class Customer(db.Model):
    """Customer of FastShop"""

    __tablename__ = "customers"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    street_address = db.Column(db.String(100), nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    state = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    country = db.Column(db.String(500), nullable=False)

    orders = db.relationship("Order", backref="customers")

    def __repr__(self):

        return "<Customer id={}, first_name={}, last_name={}, email={}>".format(self.user_id,
                                                                                self.first_name,
                                                                                self.last_name,
                                                                                self.email)
class Pickup(db.Model):
    """Pickup locations"""

    __tablename__ = "pickups"

    pickup_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    street_address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(10), nullable=False, default="NSW")
    country = db.Column(db.String(50), nullable=False, default="Australia")

    def __repr__(self):

        return "<Pickup pickup_id={}, name={}, street_address={}, zipcode={}>".format(self.pickup_id,
                                                                                      self.name,
                                                                                      self.street_address,
                                                                                      self.zipcode)

class Stores(db.Model):
    """Stores"""
    ___tablename__ = "stores"
    store_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    store_name = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
    state = db.Column(db.String(10), nullable=False, default="NSW")
    country = db.Column(db.String(50), nullable=False, default="Australia")

    stocks = db.relationship("Stock", backref="stores")

class Stock(db.Model):
    """Stock"""
    __tablename__ = "stocks"
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    stock = db.Column(db.Integer,nullable=Fallse, default=0)


class Icon(db.Model):
    """Icon for web usage"""

    __tablename__ = "icons"

    icon_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    credit = db.Column(db.String(100), nullable=False)

    def __repr__(self):

        return "<Icon icon_id={} url={} credit={}>".format(self.icon_id,
                                                           self.url,
                                                           self.credit)


class Product(db.Model):
    """Product sold by Farm to Front Door"""

    __tablename__ = "products"

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Unicode, nullable=True)  # db.Text(collation='utf8', convert_unicode=True)
    weight = db.Column(db.Numeric(asdecimal=False), nullable=True)  # db.Numeric(asdecimal=False)
    unit = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Numeric(asdecimal=False), nullable=False)  # db.Numeric(asdecimal=False)
    price_per = db.Column(db.Numeric(asdecimal=False), nullable=True)  # db.Numeric(asdecimal=False)
    per_unit = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    img = db.Column(db.String(500), nullable=True)
    icon_id = db.Column(db.Integer, db.ForeignKey('icons.icon_id'), nullable=True)
    color = db.Column(db.String(10), nullable=True)
    search_term = db.Column(db.String(50), nullable=True)
    search_strength = db.Column(db.Integer, nullable=True)

    icon = db.relationship("Icon", backref="products")

    tags = db.relationship("Tag",
                           secondary="product_tags",
                           backref="products")

    stocks = db.relationship("Stock", backref="products")

    def __repr__(self):

        return "<Product product_id={} name={} weight={} unit={} price={}>".format(self.product_id,
                                                                                   self.name,
                                                                                   self.weight,
                                                                                   self.unit,
                                                                                   self.price)
class Tag(db.Model):
    """Tag for products i.e. Certified Organic, Locally Grown"""

    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):

        return "<Tag tag_id={} name={}>".format(self.tag_id, self.name)


class Product_Tag(db.Model):
    """Association table relating Tag class to Product class"""

    __tablename__ = "product_tags"

    prod_tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)

    def __repr__(self):

        return "<Product_Tag prod_tag_id={} product_id={} tag_id={}>".format(self.prod_tag_id,
                                                                             self.product_id,
                                                                             self.tag_id)

def example_data():
    """Populate test database"""
    product = Product(name="Organic", description="Sweet and tart, these delicious blackberries are the perfect fall fruit.",
                      weight=6, unit="kg", price_per=3.99, price=3.99, per_unit="kg", aisle="Produce",
                      category="New & Peak Season", img="http://goodeggs2.imgix.net/product_photos/NmgHoSgSqmShNF10cLni_blackberries_01.jpg?w=380&h=238&fm=jpg&q=41&fit=crop",
                      icon_id=1)
    product2 = Product(name="Janet Cheese", description="Blue and mouldy",img="https://cdn.apartmenttherapy.info/image/fetch/f_auto,q_auto:eco,c_fit,w_1460/https%3A%2F%2Fstorage.googleapis.com%2Fgen-atmedia%2F3%2F2008%2F12%2F56c4f925b8e57c5babe1a0a8497a03141b2045cc.jpeg?", weight=12, unit="oz", price_per=150, price=150, per_unit="oz", aisle="Processed",
                        category="processed cheese", icon_id=2)

    icon = Icon(url="https://d30y9cdsu7xlg0.cloudfront.net/png/404999-200.png", credit="Blackberry Jam By Nikita Kozin, RU")
    tag = Tag(name="Organic")
    product_tag = Product_Tag(product_id=1, tag_id=1)
    pickup = Pickup(name="AppleWorth", description="Wednesdays: 10 a.m-3 p.m.", street_address="1/60 Frederick Street Campsie", zipcode="2194", state="NSW", country="Australia")

    db.session.add(icon)
    db.session.commit()
    db.session.add(product)
    db.session.add(product2)
    db.session.commit()
    db.session.add(pickup)
    db.session.commit()
    db.session.add(tag)
    db.session.commit()
    db.session.add(product_tag)
    db.session.commit()

def connect_to_db(app, database='postgresql://postgres:Bbklct321@localhost:5432/Beyond'):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from routes import app
    connect_to_db(app)
    db.create_all()
    example_data()
    print("Connected to DB.")