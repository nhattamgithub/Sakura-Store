from enum import unique
from linecache import lazycache
from sakura import db, login_manager
from flask_login import UserMixin
from flask import flash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    phone_num = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(120), nullable=False)
    cart = db.relationship('Cart', backref='buyer', lazy=True)

    def add_to_cart(self,product_id):
            item_to_add = Cart(product_id=product_id, user_id=self.id)
            db.session.add(item_to_add)
            db.session.commit()
            flash('Your item has been added to your cart!', 'success')
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class ProductType(db.Model):
    __tablename__ = 'producttype'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref=("type"), lazy=True)

    def __repr__(self):
        return f"ProductType('{self.type}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    product_img = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    import_price = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    supplier = db.Column(db.String(50), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('producttype.id'), nullable=False)

    def __repr__(self):
        return f"Product('{self.title}', '{self.product_img}', '{self.desc}')"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Cart('Product id:{self.product_id}','id: {self.id}','User id:{self.user_id}'')"