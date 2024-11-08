from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Product
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CreateNewProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=255)])
    price = DecimalField('Price', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    pictures = MultipleFileField('Product Pictures', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create Product')
    
    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError('Product name already exists. Please choose a different name.')
    
    def validate_price(self, price):
        if price.data <= 0:
            raise ValidationError('Price must be greater than zero.')

class EditProduct(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=255)])
    price = DecimalField('Price', validators=[DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    pictures = MultipleFileField('Product Pictures', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Product')
    

    def validate_price(self, price):
        if price.data <= 0:
            raise ValidationError('Price must be greater than zero.')