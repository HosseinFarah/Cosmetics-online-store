from . import products
from flask import render_template, redirect, url_for, request, flash, current_app, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..decorators import admin_required
from .forms import CreateNewProduct, EditProduct, CategoryForm, BrandsForm, CreateNewBrand, EditBrand, CreateNewCategory, CheckoutForm
from app.models import Product, Category, Brand, Order
from app import db
from werkzeug.utils import secure_filename
import os
import json
import stripe
from app.forms import SearchForm

# Stripe Payment Gateway Start

@products.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    form = CheckoutForm()
    if form.validate_on_submit():
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        init_basket()
        basket = session.get("basket", [])
        line_items = []
        for item in basket:
            if isinstance(item, dict) and 'price' in item and 'name' in item and 'quantity' in item:
                price = item['price']
                if item.get('discount'):
                    price = price * (1 - item['discount'] / 100)
                line_items.append({
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': item['name'],
                        },
                        'unit_amount': int(price * 100),
                    },
                    'quantity': item['quantity'],
                })
            else:
                flash('Invalid item in basket', 'error')
                return redirect(url_for('products.basket'))
        try:
            # Create or retrieve the customer
            customer = stripe.Customer.create(
                email=current_user.email,
                name=f"{current_user.firstname} {current_user.lastname}"
            )
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=url_for('products.payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('products.payment_cancel', _external=True),
                customer=customer.id,
                client_reference_id=current_user.id,
                metadata={
                    'user_full_name': f"{current_user.firstname} {current_user.lastname}"
                }
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return str(e)
    flash('Invalid CSRF token', 'danger')
    return redirect(url_for('products.basket'))

@products.route('/payment-success')
@login_required
def payment_success():
    flash('Payment successful!', 'success')
    checkout_session_id = request.args.get('session_id')
    if checkout_session_id:
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        handle_checkout_session(checkout_session)
    session.pop('basket', None)
    return redirect(url_for('auth.profile'))

@products.route('/payment-cancel')
@login_required
def payment_cancel():
    flash('Payment canceled.', 'danger')
    return redirect(url_for('products.basket'))

@products.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = current_app.config['STRIPE_ENDPOINT_SECRET']
    event = None

    # print("Webhook received")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        # print(f"Received event: {event['type']}")
    except ValueError as e:
        # print("Invalid payload")
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # print("Invalid signature")
        return 'Invalid signature', 400

    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        # print(f"Checkout session completed: {checkout_session}")
        handle_checkout_session(checkout_session)

    return '', 200

def handle_checkout_session(checkout_session):
    # Retrieve the basket from the session
    basket = session.get("basket", [])
    user_id = checkout_session.get('client_reference_id')
    if not user_id:
        print("User ID not found in checkout session")
        return

    print(f"Processing order for user ID: {user_id}")
    print(f"Checkout session ID: {checkout_session['id']}")
    print(f"Basket contents: {basket}")

    total_amount = sum(
        item['quantity'] * (item['price'] * (1 - item['discount'] / 100)) if item.get('discount') else item['quantity'] * item['price']
        for item in basket
    )
    purchased_products = [{'id':item['id'],'name': item['name'], 'price': item['price'], 'discount': item.get('discount', 0), 'quantity': item['quantity']} for item in basket]

    order = Order(
        payment_id=checkout_session['id'],
        user_id=user_id,
        total_amount=total_amount,
        purchased_products=json.dumps(purchased_products),
        status='completed'
    )
    db.session.add(order)
    db.session.commit()
    print(f"Order {order.id} added to the database")
    
    
    # Stripe Payment Gateway End

@products.route('/create_new_product', methods=['GET', 'POST'])
@login_required
@admin_required
def create_new_product():
    form = CreateNewProduct()
    brands = db.session.query(Brand).all()
    form.brand.choices = [(brand.name, brand.name) for brand in brands]
    categories = db.session.query(Category).all()
    form.category.choices = [(category.id, category.name) for category in db.session.query(Category).filter_by(parent_id=None).all()]
    form.subcategory.choices = [(subcategory.id, subcategory.name) for category in categories for subcategory in category.subcategories]
    if form.validate_on_submit():
        image = request.files['image']
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['PRODUCT_IMAGE_FOLDER'], image_filename))
        pictures = request.files.getlist('pictures')
        picture_filenames = []
        for picture in pictures:
            if picture:
                picture_filename = secure_filename(picture.filename)
                picture.save(os.path.join(current_app.config['PRODUCT_IMAGE_FOLDER'], picture_filename))
                picture_filenames.append(picture_filename)
        brand = db.session.query(Brand).filter_by(name=form.brand.data).first()
        product = Product(name=form.name.data, price=form.price.data, description=form.description.data, image=image_filename, pictures=json.dumps(picture_filenames), instructions=form.instructions.data, ingredients=form.ingredients.data, size=form.size.data, weight=form.weight.data, ean=form.ean.data, category_id=form.category.data, brand=brand,videos=form.videos.data,subcategory_id=form.subcategory.data)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('products/create_new_product.html', form=form)


    
def init_basket():
    if "basket" not in session:
        session["basket"] = []
    else:
        # Remove invalid items from the basket
        session["basket"] = [item for item in session["basket"] if isinstance(item, dict) and 'id' in item and 'name' in item and 'price' in item and 'quantity' in item]
        session.modified = True

@products.route("/add_to_basket/<int:id>")
def add_to_basket(id):
    init_basket()
    product = db.session.query(Product).get(id)
    
    if product:
        # Debugging statement to check the contents of session["basket"]
        # print("Basket contents before adding:", session["basket"])
        
        # Check if the product is already in the basket
        for item in session["basket"]:
            if isinstance(item, dict) and int(item["id"]) == int(product.id):
                item["quantity"] = item.get("quantity", 1) + 1
                session.modified = True
                flash("From this product, another product was added to the shopping cart", "success")
                break
        else:
            # If the product is not in the basket, add it with quantity 1
            session["basket"].append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image": product.image,
                "category_id": product.category_id,
                "brand": product.brand_id,
                "discount": product.get_discount_percent(),
                "quantity": 1
            })
            session.modified = True
            flash("Product added to basket", "success")
        
        # Debugging statement to check the contents of session["basket"]
        print("Basket contents after adding:")
        for item in session.get("basket", []):
            print(item.get("name"))
    else:
        flash("Product not found", "danger")
        print(f"Product with id {id} not found.")
        
    return redirect(url_for("products.brand", brand_name=product.brand.name) if product else url_for("main.index"))


@products.route("/basket/increment/<int:id>")
def increment_product(id):
    for item in session.get("basket", []):
        if isinstance(item, dict) and item.get("id") == id:
            item["quantity"] = item.get("quantity", 1) + 1
            break
    session.modified = True
    return redirect(url_for("products.basket"))

@products.route("/basket/decrement/<int:id>")
def decrement_product(id):
    for item in session.get("basket", []):
        if isinstance(item, dict) and item.get("id") == id:
            if item.get("quantity", 1) > 1:
                item["quantity"] -= 1
            else:
                session["basket"].remove(item)
            break
    session.modified = True
    return redirect(url_for("products.basket"))


@products.route("/basket")
def basket():
    init_basket()
    basket = []
    for item in session["basket"]:
        if isinstance(item, dict):
            item.setdefault("quantity", 1)
            item.setdefault("discount", 0)  # Ensure discount key exists
            basket.append(item)
        
    total = sum(
        item["quantity"] * (item["price"] * (1 - item["discount"] / 100)) if item["discount"] else item["quantity"] * item["price"]
        for item in basket
    )
    form = CheckoutForm()
    return render_template("products/basket.html", basket=basket, total=total, form=form)



@products.route("/remove_from_basket/<int:id>")
def remove_from_basket(id):
    init_basket()
    session["basket"] = [item for item in session["basket"] if not (isinstance(item, dict) and item["id"] == id)]
    session.modified = True
    return redirect(url_for("products.basket"))
        
@products.route("/edit_product/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_product(id):
    product = db.session.query(Product).get(id)
    form = EditProduct(obj=product)
    brands = db.session.query(Brand).all()
    form.brand.choices = [(brand.name, brand.name) for brand in brands]
    categories = db.session.query(Category).all()
    form.category.choices = [(category.id, category.name) for category in db.session.query(Category).filter_by(parent_id=None).all()]
    form.subcategory.choices = [(subcategory.id, subcategory.name) for category in categories for subcategory in category.subcategories]
    if form.validate_on_submit():
        image = request.files["image"]
        if image:
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config["PRODUCT_IMAGE_FOLDER"], image_filename))
            product.image = image_filename
        picture_filenames = []
        pictures = request.files.getlist("pictures")
        for picture in pictures:
            if picture:
                picture_filename = secure_filename(picture.filename)
                picture.save(os.path.join(current_app.config["PRODUCT_IMAGE_FOLDER"], picture_filename))
                picture_filenames.append(picture_filename)
        if not picture_filenames:
            picture_filenames = json.loads(product.pictures)
        
        brand = db.session.query(Brand).filter_by(name=form.brand.data).first()

        product.brand_id = brand.id
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.pictures = json.dumps(picture_filenames)
        product.instructions = form.instructions.data
        product.ingredients = form.ingredients.data
        product.size = form.size.data
        product.weight = form.weight.data
        product.ean = form.ean.data
        product.videos = form.videos.data
        product.discount = form.discount.data
        product.category_id = form.category.data
        product.subcategory_id = form.subcategory.data


        # Commit the changes
        db.session.commit()
        flash("Product updated successfully", "success")
        return redirect(url_for("main.index", id=id))
    elif request.method == "GET":
        
        brand = db.session.query(Brand).get(product.brand_id)

        
        if brand:
            form.brand.data = brand.name


        form.name.data = product.name
        form.price.data = product.price
        form.description.data = product.description
        form.instructions.data = form.instructions.data
        form.ingredients.data = product.ingredients
        form.size.data = product.size
        form.weight.data = product.weight
        form.ean.data = product.ean
        form.category.data = product.category_id
        form.subcategory.data = product.subcategory_id
        form.videos.data = product.videos
        form.discount.data = product.discount

        
    return render_template("products/edit_product.html", form=form, product=product, pictures=json.loads(product.pictures))

        
        



@products.route("/delete_product/<int:id>")
@login_required
@admin_required
def delete_product(id):
    product = db.session.query(Product).get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully", "success")
    return redirect(url_for("main.index"))

@products.route("/product/<int:id>")
def product(id):
    product = db.session.query(Product).get(id)
    brand = product.brand
    return render_template("products/product.html", product=product, pictures=json.loads(product.pictures), brand=brand)


@products.route("/category/<string:category_name>", methods=["GET", "POST"])
def category(category_name):
    form = CategoryForm()
    categories = db.session.query(Category).filter_by(parent_id=None).all()
    form.category.choices = [(c.name, c.name) for c in categories]
    category = db.session.query(Category).filter_by(name=category_name).first()
    
    if form.validate_on_submit():
        selected_category = form.category.data
        return redirect(url_for("products.category", category_name=selected_category))
    
    # Set the form data to the selected category
    form.category.data = category.name if category else None
    # Filter products based on the selected category
    products = db.session.query(Product).filter_by(category=category).all() if category else []
    brands = db.session.query(Brand).all()
    return render_template("products/category.html", products=products, categories=categories, form=form, category=category, brands=brands)
    
    
    
@products.route("/brand/<string:brand_name>", methods=["GET", "POST"])
def brand(brand_name):
    form = BrandsForm()
    
    brands = db.session.query(Brand).all()
    form.brand.choices = [(b.name, b.name) for b in brands]
    
    from collections import defaultdict
    grouped_brands = defaultdict(list)
    for brand in brands:
        first_letter = brand.name[0].upper()
        grouped_brands[first_letter].append(brand)
        
    if form.validate_on_submit():
        selected_brand = form.brand.data
        return redirect(url_for("products.brand", brand_name=selected_brand))
    
    # Get the Brand instance
    brand = db.session.query(Brand).filter_by(name=brand_name).first()
    # Filter products based on the selected brand
    form.brand.data = brand.name if brand else None
    product = db.session.query(Product).filter_by(brand=brand).first()
    
    products = db.session.query(Product).filter_by(brand=brand).all() if brand else []
    return render_template("products/brand.html", products=products, brands=brands, form=form, brand=brand,grouped_brands=grouped_brands,product=product)
    

    
@products.route("/new_brand", methods=["GET", "POST"])
@login_required
@admin_required
def new_brand():
    form = CreateNewBrand()
    if form.validate_on_submit():
        logo_filename = None
        video_filename = None
        logo = request.files["logo"]
        if logo:
            logo_filename = secure_filename(logo.filename)
            logo.save(os.path.join(current_app.config["BRAND_FOLDER"], logo_filename))
        video = request.files["video"]
        if video:
            video_filename = secure_filename(video.filename)
            video.save(os.path.join(current_app.config["BRAND_FOLDER"], video_filename))
        brand = Brand(name=form.name.data, logo=logo_filename, video=video_filename, summary=form.summary.data, description=form.description.data)
        db.session.add(brand)
        db.session.commit()
        flash("Brand created successfully", "success")
        return redirect(url_for("main.index"))
    return render_template("products/new_brand.html", form=form)

@products.route("/edit_brand/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_brand(id):
    brand = db.session.query(Brand).get(id)
    form = EditBrand(obj=brand)
    if form.validate_on_submit():
        logo = request.files["logo"]
        if logo:
            logo_filename = secure_filename(logo.filename)
            logo.save(os.path.join(current_app.config["BRAND_FOLDER"], logo_filename))
            brand.logo = logo_filename
        video = request.files["video"]
        if video:
            video_filename = secure_filename(video.filename)
            video.save(os.path.join(current_app.config["BRAND_FOLDER"], video_filename))
            brand.video = video_filename
        brand.name = form.name.data
        brand.summary = form.summary.data
        brand.description = form.description.data
        db.session.commit()
        flash("Brand updated successfully", "success")
        return redirect(url_for("products.brand", brand_name=brand.name))
    elif request.method == "GET":
        form.logo.data = brand.logo
        form.video.data = brand.video
        form.name.data = brand.name
        form.summary.data = brand.summary
        form.description.data = brand.description
    return render_template("products/edit_brand.html", form=form, brand=brand)


@products.route("/add_new_category", methods=["GET", "POST"])
@login_required
@admin_required
def add_new_category():
    form = CreateNewCategory()
    form.parent_id.choices = [(0, "None")] + [(c.id, c.name) for c in db.session.query(Category).filter_by(parent_id=None).all()] 
    if form.validate_on_submit():
        category_name = form.name.data
        parent_id = form.parent_id.data
        exicting_category = db.session.query(Category).filter_by(name=category_name).first()
        if not exicting_category:
            category = Category(name=category_name, parent_id=parent_id)
            db.session.add(category)
            db.session.commit()
            flash("Category created successfully", "success")
            return redirect(url_for("products.add_new_category"))
        else:
            flash("Category already exists", "danger")
    return render_template("products/add_new_category.html", form=form)

@products.route("/all_discounted_products", methods=["GET", "POST"])
def all_discounted_products():
    products = db.session.query(Product).filter(Product.discount > 0).all()
    # Sort products by discount percentage in descending order
    sorted_products = sorted(products, key=lambda p: p.get_discount_percent(), reverse=True)
    return render_template("products/all_discounted_products.html", products=sorted_products)



@products.route("/brands", methods=["GET"])
def brands():
    brands = db.session.query(Brand).all()
    return render_template("products/brands.html", brands=brands)

