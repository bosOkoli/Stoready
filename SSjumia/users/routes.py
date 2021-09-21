from flask_login.utils import login_required
from SSjumia.models import Order_items
from operator import index
from SSjumia.users.utils import handle_cart
from flask import Blueprint,url_for,redirect,render_template,flash,session
from flask_login import current_user,login_user
from werkzeug.wrappers import request
from SSjumia import bcrypt,db
from SSjumia.models import User,Product,Order
from SSjumia.users.forms import RegistrationForm,LoginForm,AddToCart,OrderForm
import random



users=Blueprint("users",__name__)


@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hash_pw,first_name=form.first_name.data,last_name=form.last_name.data,phone_num=form.phone_num.data,address=form.address.data,city=form.city.data,state=form.state.data,country=form.country.data)
        db.session.add(user)
        db.session.commit()
        flash('An account has been created for {username.data}. You can now log in!','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='register',form=form)


@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user)
          next_page=request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login Unsuccessful.Please check username and password','danger')
    return render_template('login.html',title='login',form=form)



@users.route('/product/view/<id>')
def view_product(id):
    form=AddToCart()
    product=Product.query.filter_by(id=id).first()

    return render_template('view-product.html',title='view-product',form=form,product=product)


@users.route('/quick-add/<id>')
def quick_add(id):
    if 'cart' not in session['cart']:
        session['cart']=[]
    session['cart'].append({'id':id,'quantity':1})
    return redirect(url_for('main.home'))


@users.route('/add-to-cart',methods=['POST'])
def add_to_cart():
    form=AddToCart()
    if 'cart' not in session:
        session['cart']=[]
    if form.validate_on_submit():
        session['cart'].append({'id':form.product_id.data,'quantity':form.quantity.data})
        session.modified=True
        return redirect(url_for('main.home'))

@users.route('/cart')
def cart():

    products,grand_total,grand_total_plus_shipping,quantity_total=handle_cart()
    return render_template('cart.html',title='cart',products=products,grand_total=grand_total,grand_total_plus_shipping=grand_total_plus_shipping,quantity_total=quantity_total)

@users.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified=True
    return redirect(url_for('users.cart'))


@users.route('/cart/checkout',methods=['GET','POST'])
@login_required
def checkout():
    form=OrderForm()
    products,grand_total,grand_total_plus_shipping,quantity_total=handle_cart()
    if form.validate_on_submit(): 
        order=Order()
        user=User.query.filter_by(id=id).first()
        order=Order(username=user.username.data,email=user.email.data,first_name=user.first_name.data,last_name=user.last_name.data,phone_num=user.phone_num.data,address=user.address.data,city=user.city.data,state=user.state.data,country=user.country.data)
        order.reference=''.join([random.choice('ABCDE') for _ in range(5)])
        order.status='Pending'
        for product in products:
            order_items=Order_items(quantity=product['quantity'],product_id=product['id'])
            order.items.append(order_items)
        db.session.add(order)
        db.session.commit()
        session['cart']=[]
        session.modified=True
        return redirect('main.home')
    return render_template('checkout.html',title='Cart-checkout',form=form,products=products,grand_total=grand_total,grand_total_plus_shipping=grand_total_plus_shipping,quantity_total=quantity_total)
        
