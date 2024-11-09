from . import products
from flask import render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from ..decorators import admin_required
from .forms import CreateNewProduct, EditProduct
from app.models import Product
from app import db
from werkzeug.utils import secure_filename
import os
import json

@products.route('/create_new_product', methods=['GET', 'POST'])
@login_required
@admin_required
def create_new_product():
    form = CreateNewProduct()
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
        product = Product(name=form.name.data, price=form.price.data, description=form.description.data, image=image_filename, pictures=json.dumps(picture_filenames), instructions=form.instructions.data, ingredients=form.ingredients.data, size=form.size.data, weight=form.weight.data, ean=form.ean.data, category_id=form.category.data)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('products/create_new_product.html', form=form)


    
def init_basket():
    if "basket" not in session:
        session["basket"] = []
        
        

@products.route("/add_to_basket/<int:id>")
def add_to_basket(id):
    init_basket()
    products = db.session.query(Product).all()
    product = next((p for p in products if p.id == id), None)
    
    if product:
        # # Debugging statement to check the contents of session["basket"]
        # print("Basket contents:", session["basket"])
        
        # Check if the product is already in the basket
        for item in session["basket"]:
            try:
                # # Debugging statement to check the type of item
                # print("Item type:", type(item))
                
                if isinstance(item, dict) and int(item["id"]) == int(product.id):
                    item["quantity"] = item.get("quantity", 1) + 1
                    session.modified = True
                    flash("From this product, another product was added to the shopping cart", "success")
                    break
            except ValueError:
                flash("Invalid product ID in basket", "danger")
                return redirect(url_for("products.product", id=id))
        else:
            # If the product is not in the basket, add it with quantity 1
            session["basket"].append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image": product.image,
                "description": product.description,
                "instructions": product.instructions,
                "ingredients": product.ingredients,
                "size": product.size,
                "weight": product.weight,
                "ean": product.ean,
                "category_id": product.category_id,
                "quantity": 1
            })
            session.modified = True
            flash("Product added to basket", "success")
    else:
        flash("Product not found", "danger")
        
    return redirect(url_for("products.product", id=id))


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
            basket.append(item)
    total = sum(item["price"] * item["quantity"] for item in basket)
    return render_template("products/basket.html", basket=basket, total=total)



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
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.pictures = json.dumps(picture_filenames)
        product.instructions = form.instructions.data
        product.ingredients = form.ingredients.data
        product.size = form.size.data
        product.weight = form.weight.data
        product.ean = form.ean.data
        product.category_id = form.category.data

        # Commit the changes
        db.session.commit()
        flash("Product updated successfully", "success")
        return redirect(url_for("main.index", id=id))
        
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
    return render_template("products/product.html", product=product, pictures=json.loads(product.pictures))