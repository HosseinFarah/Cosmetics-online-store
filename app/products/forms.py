from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Product
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CreateNewProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2)])
    price = DecimalField('Price', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    pictures = MultipleFileField('Product Pictures', validators=[FileAllowed(['jpg', 'png', 'jpeg','webp'])])
    instructions = TextAreaField('Instructions', validators=[DataRequired(), Length(min=2)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired(), Length(min=2)])
    size = StringField('Size', validators=[DataRequired(), Length(min=2, max=100)])
    weight = StringField('Weight', validators=[DataRequired(), Length(min=2, max=100)])
    ean = StringField('EAN', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField('Category', choices=[(1, 'Electronics'), (2, 'Cosmetics'), (3, 'Toiletries')], coerce=int)   
    brand = SelectField('Brand', choices=[], validators=[DataRequired()])
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
    instructions = TextAreaField('Instructions', validators=[DataRequired(), Length(min=2)])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired(), Length(min=2)])
    size = StringField('Size', validators=[DataRequired(), Length(min=2, max=100)])
    weight = StringField('Weight', validators=[DataRequired(), Length(min=2, max=100)])
    ean = StringField('EAN', validators=[DataRequired(), Length(min=2, max=100)])
    brand = SelectField('Brand', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update Product')
    

    def validate_price(self, price):
        if price.data <= 0:
            raise ValidationError('Price must be greater than zero.')