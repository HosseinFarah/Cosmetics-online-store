from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField, DecimalField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Product, Brand, Category,Translation
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
    category = SelectField('Category', choices=[], coerce=int)   
    subcategory = SelectField('Subcategory', choices=[], coerce=int)
    brand = SelectField('Brand', choices=[], validators=[DataRequired()])
    videos = TextAreaField('Videos')
    submit = SubmitField('Add Product')
    
    def __init__(self, *args, **kwargs):
        super(CreateNewProduct, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.filter_by(parent_id=None).all()]
        self.subcategory.choices = []
    
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
    category = SelectField('Category', choices=[], coerce=int)
    subcategory = SelectField('Subcategory', choices=[], coerce=int)
    instructions = TextAreaField('Instructions')
    ingredients = TextAreaField('Ingredients')
    size = StringField('Size')
    weight = StringField('Weight')
    ean = StringField('EAN')
    brand = SelectField('Brand', choices=[], validators=[DataRequired()])
    videos = TextAreaField('Videos')
    discount = FloatField('Discount (%)')
    submit = SubmitField('Update Product')
    
    def __init__(self, *args, **kwargs):
        super(EditProduct, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.filter_by(parent_id=None).all()]
        self.subcategory.choices = []

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


class CreateNewCategory(FlaskForm):
    name = StringField('Category Name')
    parent_id = SelectField('Parent Category', choices=[(0, 'None')], coerce=int)
    submit = SubmitField('Add Category')
    
    def __init__(self, *args, **kwargs):
        super(CreateNewCategory, self).__init__(*args, **kwargs)
        # Populate parent categories (root categories)
        self.parent_id.choices = [(None, 'Root Category')] + [(category.id, category.name) for category in Category.query.filter_by(parent_id=None).all()]

# STRIPE Payment
class CheckoutForm(FlaskForm):
    submit = SubmitField('Proceed to Payment')

# for translation from db
class CreateTranslation(FlaskForm):
    language = SelectField('Language', coerce=str, validators=[DataRequired()])
    field = SelectField('Field', coerce=str, validators=[DataRequired()])
    text= TextAreaField('Text', validators=[DataRequired()])
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Translation')
    
class EditTranslation(FlaskForm):
    language = SelectField('Language', coerce=str, validators=[DataRequired()])
    field = SelectField('Field', coerce=str, validators=[DataRequired()])
    text= TextAreaField('Text', validators=[DataRequired()])
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Translation')



class CreateRatingForm(FlaskForm):
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Length(min=0, max=500)])
    product_id = HiddenField('Product ID')
    user_id = HiddenField('User ID')
    submit = SubmitField('Submit')


class UpdateRatingForm(FlaskForm):
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Length(min=0, max=500)])
    product_id = HiddenField('Product ID')
    user_id = HiddenField('User ID')
    submit = SubmitField('Submit')
    