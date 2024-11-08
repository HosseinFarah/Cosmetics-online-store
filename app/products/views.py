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
        product = Product(name=form.name.data, price=form.price.data, description=form.description.data, image=image_filename, pictures=json.dumps(picture_filenames))
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully')
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
        session["basket"].append({"id": product.id, "name": product.name, "price": product.price})
        session.modified = True
    return redirect(url_for("main.index"))

@products.route("/basket")
def basket():
    init_basket()
    total = sum(item["price"] for item in session["basket"] if isinstance(item, dict))
    return render_template("products/basket.html", basket=[item for item in session["basket"] if isinstance(item, dict)], total=total)

@products.route("/remove/<int:id>")
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
            else:
                picture_filenames = json.loads(product.pictures)
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.pictures = json.dumps(picture_filenames)
        db.session.commit()
        flash("Product updated successfully")
        return redirect(url_for("main.index", id=id))
    return render_template("products/edit_product.html", form=form, product=product,pictures=json.loads(product.pictures))
    
@products.route("/delete_product/<int:id>")
@login_required
@admin_required
def delete_product(id):
    product = db.session.query(Product).get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully")
    return redirect(url_for("main.index"))