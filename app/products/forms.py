from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField, DecimalField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Product, Brand
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CreateNewProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2)])
    price = DecimalField('Price', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    pictures = MultipleFileField('Product Pictures', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    instructions = TextAreaField('Instructions')
    ingredients = TextAreaField('Ingredients')
    size = StringField('Size')
    weight = StringField('Weight')
    ean = StringField('EAN')
    category = SelectField('Category', choices=[(1, 'Electronics'), (2, 'Cosmetics'), (3, 'Toiletries')], coerce=int)   
    brand = SelectField('Brand', choices=[], validators=[DataRequired()])
    videos = TextAreaField('Videos')
    submit = SubmitField('Add Product')
    
    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError('Product name already exists. Please choose a different name.')
    
    def validate_price(self, price):
        if price.data <= 0:
            raise ValidationError('Price must be greater than zero.')

class EditProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2)])
    price = DecimalField('Price', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    pictures = MultipleFileField('Product Pictures', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    category = SelectField('Category', choices=[(1, 'Electronics'), (2, 'Cosmetics'), (3, 'Toiletries')], coerce=int)
    instructions = TextAreaField('Instructions')
    ingredients = TextAreaField('Ingredients')
    size = StringField('Size')
    weight = StringField('Weight')
    ean = StringField('EAN')
    brand = SelectField('Brand', choices=[], validators=[DataRequired()])
    videos = TextAreaField('Videos')
    discount = FloatField('Discount (%)')
    submit = SubmitField('Update Product')
    

    def validate_price(self, price):
        if price.data <= 0:
            raise ValidationError('Price must be greater than zero.')
        
    def validate_discount(self, discount):
        if discount.data < 0:
            raise ValidationError('Discount must be greater than or equal to zero.')

        
class CategoryForm(FlaskForm):
    category = SelectField('Category', choices=[])
    submit = SubmitField('Go')
    
class BrandsForm(FlaskForm):
    brand = SelectField('Brand', choices=[])
    submit = SubmitField('Go')
    
    
class CreateNewBrand(FlaskForm):
    name = StringField('Brand Name')
    summary = TextAreaField('Summary')
    logo = FileField('Brand Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    video = FileField('Brand Video', validators=[FileAllowed(['mp4', 'webm'])])
    description = TextAreaField('Description')
    submit = SubmitField('Add Brand')

class EditBrand(FlaskForm):
    name = StringField('Brand Name')
    summary = TextAreaField('Summary')
    logo = FileField('Brand Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    video = FileField('Brand Video', validators=[FileAllowed(['mp4', 'webm'])])
    description = TextAreaField('Description')
    submit = SubmitField('Update Brand')