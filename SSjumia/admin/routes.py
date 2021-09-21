from SSjumia.admin.forms import AdminRegistrationForm,AdminLoginForm,AdminUploadForm,CompletedOrdersForm
from flask import Blueprint,redirect,url_for,flash
from flask.templating import render_template
from SSjumia import bcrypt,db
from SSjumia.models import *
from flask_login import login_user,current_user,login_required
from SSjumia.admin.utils import *




admin=Blueprint('admin',__name__)



@admin.route('/admin-dashboard')
@login_required
def admin_home():
   form= CompletedOrdersForm()
   orders=Order.query.order_by(Order.date_ordered.desc()).all()
   products=Product.query.order_by(Product.date_ordered.desc()).all()
   cart_products,_,_,_=handle_cart()
   if form.validate_on_submit():
       if form.complete_orders.data == True:
          order=Order.query.filter_by(Order.id).first()
          order.complete=True
          order.status='Completed'
       for product in cart_products:
            product=Product.query.filter_by(id=products['id']).update({'stock':product.stock-product['quantity']})

   return render_template('admin.html',admin=True,orders=orders,products=products)


@admin.route('/admin/register',methods=['GET','POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin.home'))
    form=AdminRegistrationForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file=save_profile_picture(form.image_file.data)
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin=Admin(username=form.username.data,email=form.email.data,password=hash_pw,role=form.role.data,image_file=image_file)
        db.session.add(admin)
        db.session.commit()
    return render_template('admin_register.html',title='admin-registration',form=form,admin=True)

@admin.route('/admin/login',methods=['GET','POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin.home'))
    form=AdminLoginForm()
    if form.validate_on_submit():
        admin=Admin.query.filter_by(form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.password,form.password.data):
            login_user(admin)
            return redirect(url_for('admin.admin.home'))
        flash('Login Unsuccessful. Check Username and Password or go get BOS','danger')
    return render_template('admin_login.html',title='admin-login',form=form,admin=True)

@admin.route('/admin/upload',methods=['GET','POST'])
@login_required
def admin_post():
    form=AdminUploadForm()
    if form.validate_on_submit:
        if form.image_file.data:
            image_file=save_product_image_file(form.image_file.data)
        if form.category.data=='electronics':
            product=Product(image_file=image_file,prod_name=form.Prod_name.data,prod_desc=form.prod_desc.data,prod_price=form.prod_price.data,prod_stock=form.prod_stock.data,cat_id=1)
            db.session.add(product)
            db.session.commit()
        elif form.category.data=='food':
            product=Product(image_file=image_file,prod_name=form.Prod_name.data,prod_desc=form.prod_desc.data,prod_price=form.prod_price.data,prod_stock=form.prod_stock.data,cat_id=2)
            db.session.add(product)
            db.session.commit()
        elif form.category.data=='fashion':
            product=Product(image_file=image_file,prod_name=form.Prod_name.data,prod_desc=form.prod_desc.data,prod_price=form.prod_price.data,prod_stock=form.prod_stock.data,cat_id=3)
            db.session.add(product)
            db.session.commit()
        elif form.category.data=='health':
            product=Product(image_file=image_file,prod_name=form.Prod_name.data,prod_desc=form.prod_desc.data,prod_price=form.prod_price.data,prod_stock=form.prod_stock.data,cat_id=4)
            db.session.add(product)
            db.session.commit()
        elif form.category.data=='household':
            product=Product(image_file=image_file,prod_name=form.Prod_name.data,prod_desc=form.prod_desc.data,prod_price=form.prod_price.data,prod_stock=form.prod_stock.data,cat_id=5)
            db.session.add(product)
            db.session.commit()
        elif form.category.data=='toletries':
            product=Product(image_file=image_file,prod_name=form.Prod_name.data,prod_desc=form.prod_desc.data,prod_price=form.prod_price.data,prod_stock=form.prod_stock.data,cat_id=6)
            db.session.add(product)
            db.session.commit()
        flash('This Product has been added successfully!','success')
        return redirect(url_for('main.home'))
    return render_template('admin_upload.html',admin=True)

@admin.route('/admin/users')
def admin_users():
    users=User.query.all()
    return render_template('admin_users',admin=True,users=users)

@admin.route('/admin/pending-orders')
def pending_orders():
    orders=Order.query.order_by(Order.date_ordered.desc()).all()
    for order in orders:
        if order.complete is False:
            return order
    return render_template('pending_orders.html',title='pending-orders',order=order)


@admin.route('/admin/completed-orders')
def completed_orders():
    orders=Order.query.order_by(Order.date_ordered.desc()).all()
    for order in orders:
        if order.complete is True:
            return order
    return render_template('completed_orders.html',title='completed-orders',order=order)

