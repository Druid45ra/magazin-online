from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
import os
import logging
from werkzeug.utils import secure_filename
from models import db, User, Product, CartItem
from forms import ProductForm, LoginForm, RegistrationForm

# Configurarea aplicației
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Configurare logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inițializare extensii
db.init_app(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Crearea folderului pentru încărcare imagini
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Funcții utile
def save_product_image(image):
    if image and '.' in image.filename and \
       image.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        return f'uploads/{filename}'
    return None

# Rutele aplicației
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produse')
def produse():
    produse = Product.query.all()
    return render_template('produse.html', produse=produse)

@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    existing_cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing_cart_item:
        existing_cart_item.quantity += 1
    else:
        new_cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    flash('Produs adăugat în coș', 'success')
    return redirect(url_for('produse'))

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image = form.image.data
        image_path = save_product_image(image) if image else None
        new_product = Product(
            name=form.name.data, 
            price=form.price.data, 
            description=form.description.data,
            image_path=image_path
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Produs adăugat cu succes!', 'success')
        return redirect(url_for('produse'))
    return render_template('add_product.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Autentificare reușită!', 'success')
            return redirect(url_for('index'))
        flash('Username sau parolă incorectă', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Înregistrare reușită!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Te-ai deconectat cu succes', 'success')
    return redirect(url_for('login'))

# Crearea bazei de date
with app.app_context():
    db.create_all()
    logger.info("Bazele de date au fost create cu succes.")

if __name__ == '__main__':
    app.run(debug=True)
