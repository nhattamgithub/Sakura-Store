import os
import datetime
from datetime import date
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from numpy import result_type
from sakura import app, db, bcrypt
from sakura.models import User, Product, ProductType, Cart
from sakura.forms import SearchForm, ProductTypeForm, RegistrationForm, LoginForm, UpdateAccountForm, ProductForm, Types
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    products = Product.query.all()
    types = enumerate(Types())
    return render_template("home.html",products=products,types=types)

@app.route("/base", methods=['GET', 'POST'])
def base():
    cart = Cart.query.all()
    count = 0
    for item in cart:
        count += 1
    return render_template("base.html",count=count)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, phone_num=form.phone_num.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash('Bạn đã tạo tài khoản thành công, đăng nhập ngay bây giờ được luôn đó ~!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Sai email hoặc mật khẩu rồi :( Kiểm tra lại bạn nhé ~!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (433, 433)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_num = form.phone_num.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Cập nhật thông tin của quý khách hàng thành công~!')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_num.data = current_user.phone_num
        form.address.data = current_user.address
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/type/add", methods=['GET', 'POST'])
@login_required
def new_type():
    if current_user.email == 'admin@gmail.com':
        form = ProductTypeForm()
        if form.validate_on_submit():
            type = ProductType(type = form.type.data)
            db.session.add(type)
            db.session.commit()
        return render_template('add_type.html',title='Add Type', form=form)    

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    products = Product.query.all()
    types = enumerate(Types())
    if current_user.email == 'admin@gmail.com':
        return render_template("admin.html",products=products,types=types)


@app.route("/adminfilter/<int:type_id>", methods=['GET', 'POST'])
@login_required
def adminfilter(type_id):
    products = Product.query.filter_by(type_id = type_id)
    types = enumerate(Types())
    if current_user.email == 'admin@gmail.com':
        return render_template("adminfilter.html",products=products,types=types)

@app.route("/product/add", methods=['GET', 'POST'])
@login_required
def new_product():
    if current_user.email == 'admin@gmail.com':
        form = ProductForm()
        if form.validate_on_submit():
            product = Product()
            product.product_img = save_picture(form.product_img.data)
            product.title = form.title.data
            product.desc = form.desc.data
            product.price = form.price.data
            product.import_price = form.import_price.data
            product.quantity = form.quantity.data
            product.supplier = form.supplier.data
            product.material = form.material.data
            product.size = form.size.data
            product.mass = form.mass.data
            for index, product_type in enumerate(Types()):
                if form.type.data == product_type:
                    product.type_id = index + 1
            db.session.add(product)
            db.session.commit()
            flash('Bạn đã thêm sản phẩm thành công~!','success')
        return render_template('add_product.html',title='Add product', form=form)
                
@app.route("/product/update/<int:product_id>", methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    if current_user.email == 'admin@gmail.com':
        product = Product.query.get_or_404(product_id)
        form = ProductForm()
        if form.validate_on_submit():
            product.product_img = save_picture(form.product_img.data)
            product.title = form.title.data
            product.desc = form.desc.data
            product.price = form.price.data
            product.import_price = form.import_price.data
            product.quantity = form.quantity.data
            product.supplier = form.supplier.data
            product.material = form.material.data
            product.size = form.size.data
            product.mass = form.mass.data
            for index, type_name in enumerate(Types()):
                if form.type.data == type_name:
                    product.type_id = index + 1
            db.session.commit()
            flash('Bạn đã cập nhật sản phẩm thành công~!','success')
            return redirect(url_for('admin'))
        elif request.method == 'GET':
            form.title.data = product.title
            form.product_img.data = product.product_img
            form.desc.data = product.desc
            form.price.data = product.price
            form.import_price.data = product.import_price
            form.quantity.data = product.quantity
            form.supplier.data = product.supplier
            form.material.data = product.material
            form.size.data = product.size
            form.mass.data = product.mass

        return render_template('add_product.html', title='Update product',form=form)

@app.route("/product/delete/<int:product_id>", methods=['GET','POST'])
@login_required
def delete_product(product_id):
    if current_user.email == 'admin@gmail.com':
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('Bạn đã xóa sản phẩm thành công~!','success')
        return redirect(url_for('admin'))


@app.route("/products/<int:type_id>", methods=['GET','POST'])
def product(type_id):
    products = Product.query.filter_by(type_id = type_id)
    for index, product_type in enumerate(Types()):
        if index == type_id - 1:
            type_name = product_type
    return render_template('products.html',products=products,type_name=type_name)

@app.route("/product-detail/<int:product_id>", methods=['GET','POST'])
def product_detail(product_id):
    products = Product.query.filter_by(id = product_id)
    for product in products:
        for index, product_type in enumerate(Types()):
            if index == product.type_id - 1:
                type_name = product_type
    
    return render_template('product_detail.html',products=products,type_name=type_name)

@app.route("/addToCart/<int:product_id>")
@login_required
def addToCart(product_id):
    row = Cart.query.filter_by(product_id=product_id, buyer=current_user).first()
    if row:
        row.quantity += 1
        db.session.commit()
        flash('Sản phẩm này đã tồn tại trong giỏ hàng của bạn, cộng thêm 1 cho bạn nè~!', 'success')
    else:
        user = User.query.get(current_user.id)
        user.add_to_cart(product_id)
    return redirect(url_for('home'))

@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    user = current_user
    today = date.today()
    receive_day = today + datetime.timedelta(days=3)
    receive_day = receive_day.strftime("%d/%m/%Y")
    cart = Product.query.join(Cart).add_columns(Cart.quantity, Product.price, Product.title, Product.product_img, Product.id).filter_by(buyer=current_user).all()
    subtotal = 0
    for item in cart:
        subtotal+=int(item.price)*int(item.quantity)
    subtotal+=30000
    if request.method == "POST":
        qty = request.form.get("qty")
        idpd = request.form.get("idpd")
        cartitem = Cart.query.filter_by(product_id=idpd).first()
        cartitem.quantity = qty
        db.session.commit()
        cart = Product.query.join(Cart).add_columns(Cart.quantity, Product.price, Product.title, Product.product_img, Product.id).filter_by(buyer=current_user).all()
        subtotal = 0
        for item in cart:
            subtotal+=int(item.price)*int(item.quantity)
        subtotal+=30000
    return render_template('cart.html',receive_day=receive_day, cart=cart, subtotal=subtotal,user=user)

@app.route("/removeFromCart/<int:product_id>")
@login_required
def removeFromCart(product_id):
    item_to_remove = Cart.query.filter_by(product_id=product_id, buyer=current_user).first()
    db.session.delete(item_to_remove)
    db.session.commit()
    flash('Bạn đã xóa sản phẩm thành công!', 'success')
    return redirect(url_for('cart'))

