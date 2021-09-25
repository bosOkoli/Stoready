from itertools import product
from flask_login.utils import login_required
from SSjumia.models import Order_items
from flask import Blueprint,url_for,redirect,render_template,flash,session,request
from flask_login import current_user,login_user,logout_user
from SSjumia import bcrypt,db
from SSjumia.models import User,Product,Order
from SSjumia.users.forms import RegistrationForm,LoginForm,AddToCart,OrderForm,RequestResetForm,ResetPasswordForm,UpdateAccountForm
import random
from SSjumia.users.utils import send_reset_email



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
        flash(f'An account has been created for {form.username.data}. You can now log in!','success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html',title='register',form=form)


@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= LoginForm()
    if form.validate_on_submit():
        for user in User.query.filter_by(username=form.username.data):
                if user and bcrypt.check_password_hash(user.password,form.password.data):
                   login_user(user,remember=form.remember.data)
                   next_page=request.args.get('next')
                   return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Login Unsuccessful.Please check username and password','danger')
    return render_template('users/login.html',title='login',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/product/view/<id>')
def view_product(id):
    form=AddToCart()
    product=Product.query.filter_by(id=id).first()

    return render_template('main/view_product.html',title='view-product',form=form,product=product)


@users.route('/quick-add/<id>')
def quick_add(id):
    if 'cart' not in session:
        session['cart']=[]
    session['cart'].append({'id':id,'quantity':1})
    session.modified=True
    if current_user.is_authenticated:
       session.permanent=True   
    return redirect(url_for('main.home'))


@users.route('/add-to-cart',methods=['POST'])
def add_to_cart():
    form=AddToCart()
    if 'cart' not in session:
        session['cart']=[]
    if form.validate_on_submit():
        session['cart'].append({'id':form.product_id.data,'quantity':form.quantity.data})
        session.modified=True
        if current_user.is_authenticated:
           session.permanent=True
        return redirect(url_for('main.home'))

def handle_cart():
    products=[]
    grand_total=0
    index=0
    quantity_total=0
    for item in session['cart']:
        product=Product.query.filter_by(id=item['id']).first()   
        quantity=int(item['quantity'])
        total=quantity*product.prod_price
        grand_total+=total
        grand_total_plus_shipping=grand_total + 1500
        products.append({'id':product.id,'name':product.prod_name,'price':product.prod_price,'image':product.image_file,'quantity':quantity,'total':total,'index':index})
        index+=1
        quantity_total+=quantity
        
        return products,grand_total ,grand_total_plus_shipping,quantity_total

@users.route('/cart')
def cart():
    products=[]
    grand_total=0
    index=0
    for item in session['cart']:
        product=Product.query.filter_by(id=item['id']).first()

        quantity= int(item['quantity'])

        total=quantity * product.prod_price
        grand_total+=total
        grand_total_plus_shipping=grand_total+1500

        products.append({'id':product.id,'name':product.prod_name,'price':product.prod_price,'quantity':quantity,'total':total,'image':product.image_file,'index':index})
        index+=1
    if session['cart']==[]:
        return redirect(url_for('main.home'))
    return render_template('main/cart.html',title='cart',products=products,grand_total=grand_total,grand_total_plus_shipping=grand_total_plus_shipping)

@users.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified=True
    if session['cart']==[]:
        return redirect(url_for('main.home'))
    return redirect(url_for('users.cart'))


@users.route('/cart/checkout',methods=['GET','POST'])
@login_required
def checkout():
    form=OrderForm()
    products=[]
    grand_total=0
    index=0
    for item in session['cart']:
        product=Product.query.filter_by(id=item['id']).first()

        quantity= int(item['quantity'])

        total=quantity * product.prod_price
        grand_total+=total
        grand_total_plus_shipping=grand_total+1500

        products.append({'id':product.id,'name':product.prod_name,'price':product.prod_price,'quantity':quantity,'total':total,'image':product.image_file,'index':index})
    if form.validate_on_submit():
        order=Order()
        user=current_user
        order=Order(username=user.username,email=user.email,first_name=user.first_name,last_name=user.last_name,phone_num=user.phone_num,address=user.address,city=user.city,state=user.state,country=user.country,payment_type=form.payment_type.data,user_id=user.id)
        order.reference=''.join([random.choice('ABCDE') for _ in range(5)])
        order.status='Pending'
        for product in products:
            order_items=Order_items(quantity=product['quantity'],product_id=product['id'])
            order.items.append(order_items)
        db.session.add(order)
        db.session.commit()
        session['cart']=[]
        session.modified=True
        flash('Your Order has been placed!','success')
        return redirect(url_for('main.home'))
    return render_template('main/checkout.html',title='Cart-checkout',form=form,products=products,grand_total=grand_total,grand_total_plus_shipping=grand_total_plus_shipping)
        
@users.route("/reset_password",methods = ["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html',title= 'Request Password Reset', form=form)


@users.route("/reset_password/<token>",methods = ["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user= User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form= ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed_pw
        db.session.commit()
        flash(f'Your password has been successfully updated!. Your can now log in!','success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_token.html',title= 'Request Password Reset', form=form)

@users.route("/account",methods=["GET","POST"])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
       current_user.username=form.username.data
       current_user.email=form.email.data
       current_user.address=form.address.data
       current_user.phone_num=form.phone_num.data
       current_user.city=form.city.data
       current_user.state=form.state.data
       db.session.commit()
       flash('Your Account has been updated successfully!','success')
       return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data=current_user.address
        form.phone_num.data=current_user.phone_num
        form.city.data=current_user.city
        form.state.data=current_user.state
    return render_template('users/account.html',title='Account Info',form=form)

@users.route("/orders")
def orders():
    page= request.args.get('page',1,type=int)
    user=User.query.filter_by(username=current_user.username).first_or_404()
    orders=Order.query.filter_by(author=user).order_by(Order.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('users/view_orders.html', orders=orders,user=user)



