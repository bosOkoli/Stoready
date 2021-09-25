from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref
from SSjumia import db,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__='user'
    id= db.Column(db.Integer,unique=True,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    first_name=db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    phone_num=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(50),nullable=False)
    state=db.Column(db.String(50),nullable=False)
    country=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    order=db.relationship('Order',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None 
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.first_name}','{self.last_name}')"

class Category(db.Model):
       __tablename__="categories"
       id= db.Column(db.Integer,unique=True,primary_key=True)
       name=db.Column(db.String(20),nullable=False)
       description=db.Column(db.String(1000),nullable=False)
       product=db.relationship('Product',backref='categories',lazy=True)
       


class Product(db.Model):
    __tablename__="product"
    id=db.Column(db.Integer,unique=True,primary_key=True)
    image_file=db.Column(db.String(500),nullable=False,default="default.jpg")
    prod_name=db.Column(db.String(20),nullable=False)
    prod_price=db.Column(db.Integer,nullable=False)
    product_desc=db.Column(db.Text,nullable=False)
    cat_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    prod_stock=db.Column(db.Integer)
    category=db.relationship('Category',backref='cat_posts',foreign_keys=[cat_id])
    orders=db.relationship('Order_items',backref='product',lazy=True)
    
    def __repr__(self):
        return f'Post("{self.prod_name},{self.category},{self.image_file}")'


class Order(db.Model):
    __tablename__='order'
    id=db.Column(db.Integer,unique=True,primary_key=True,nullable=False)
    username=db.Column(db.String(50),nullable=False)
    first_name=db.Column(db.String(50),nullable=False)
    last_name=db.Column(db.String(50),nullable=False)
    phone_num=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(50),nullable=False)
    state=db.Column(db.String(50),nullable=False)
    country=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    reference=db.Column(db.String(10),nullable=False)
    status=db.Column(db.String(20),nullable=False)
    payment_type=db.Column(db.String(20),nullable=False)
    complete=db.Column(db.Boolean,default=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    items=db.relationship('Order_items',backref='order',lazy=True)

    def order_total(self):
        return db.session.query(db.func.sum(Order_items.quantity*Product.prod_price)).join(Product).filter(Order_items.order_id==self.id).scalar()
    
    def quantity_total(self):
        return db.session.query(db.func.sum(Order_items.quantity)).filter(Order_items.order_id==self.id).scalar()

    def __repr__(self):
        return f"Order('{self.first_name}','{self.last_name}','{self.phone_num}','{self.email}')"

class Order_items(db.Model):
    __tablename__='order_items'
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    order_id=db.Column(db.Integer,db.ForeignKey('order.id'),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        return f"Order_items('{self.order_id}','{self.product_id}','{self.quantity}')"

