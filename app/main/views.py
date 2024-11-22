from . import main
from flask import render_template, redirect, url_for, request, flash, current_app, session, g
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Todo, Product, Category, Brand, Ticket
from app import db
from app.forms import SearchForm
from sqlalchemy import or_
from flask_babel import get_locale as babel_get_locale

# @main.route('/')
# @main.route('/index')
# @login_required
# def index():
#     return render_template('index.html', title='Todo App' , todos=Todo.query.filter_by(user_id=current_user.id).all())



# Search form in the base.html
@main.app_context_processor
def inject_search_form():
    return dict(form=SearchForm())

# Open tickets count in the base.html
@main.app_context_processor
def inject_open_tickets_count():
    if current_user.is_administrator():
        open_tickets_count = Ticket.query.filter_by(status='open').count()
    elif current_user.is_authenticated:
        open_tickets_count = Ticket.query.filter_by(status='open', user_id=current_user.id).count()
    else:
        open_tickets_count = None

    return dict(open_tickets_count=open_tickets_count)

# for translation
@main.before_app_request
def before_request():
    g.locale = babel_get_locale()
    # current_app.logger.info(f"Current locale: {g.locale}")
    if 'lang' in session:
        g.locale = session['lang']
    else:
        g.locale = request.accept_languages.best_match(current_app.config['BABEL_SUPPORTED_LOCALES'])
    current_app.logger.info(f"Locale set to: {g.locale}")
    
    
    
# for translation
@main.route('/set_language', methods=['POST'])
def set_language():
    lang_code = request.form.get('lang_code')
    if lang_code:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('main.index'))



@main.route("/")
def index():
    products = Product.query.all()
    categories = Category.query.all()
    sliders = ['(1).webp', '(2).webp', '(3).webp', '(4).webp']
    return render_template("index.html", products=products, categories=categories, sliders=sliders, title='Home')

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search = form.search.data.strip()
        products = db.session.query(Product).filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%'),
                Product.ingredients.ilike(f'%{search}%'),
                Product.instructions.ilike(f'%{search}%'),
                Product.size.ilike(f'%{search}%'),
                Product.weight.ilike(f'%{search}%'),
                Product.ean.ilike(f'%{search}%')
            )
        ).all()
        brands = db.session.query(Brand).filter(Brand.name.ilike(f'%{search}%')).all()
    return render_template('search.html', products=products, brands=brands, form=form)