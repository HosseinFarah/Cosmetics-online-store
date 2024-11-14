
from flask import render_template
from .models import Product

@app.route('/all_discounted_products')
def all_discounted_products():
    products = Product.query.all()
    # Sort products by discount percentage in descending order
    sorted_products = sorted(products, key=lambda p: p.get_discount_percent(), reverse=True)
    return render_template('products/all_discounted_products.html', products=sorted_products)