from SSjumia.users.routes import *
from SSjumia.models import Product


def handle_cart():
    products=[]
    grand_total=0
    index=0
    quantity_total=0
    for item in session['cart']:
        product=Product.query.filter_by(id=item['id']).first()   
        quantity=int(item['quantity'])
        total=quantity*product.price
        grand_total+=total
        grand_total_plus_shipping=grand_total + 2000
        products.append({'id':product.id,'name':product.name,'price':product.price,'image':product.image_file,'quantity':quantity,'total':total,'index':index})
        index+=1
        quantity_total+=quantity
        
        return total,grand_total ,grand_total_plus_shipping,quantity_total