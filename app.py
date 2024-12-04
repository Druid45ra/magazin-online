from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# Configurarea aplicației
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cheie secretă pentru Flask-WTF
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Clasa utilizatorului
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

# Simulăm o bază de date de utilizatori
users = {
    "testuser": User(1, "testuser", bcrypt.generate_password_hash("testpassword").decode('utf-8'))
}

# Clase de formulare
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

# Rute
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Attempting login for user: {form.username.data}")
        user = users.get(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Autentificare reușită!', 'success')
            return redirect(url_for('index'))
        else:
            print("Login failed: Invalid credentials")
            flash('Username sau parolă incorectă', 'danger')
    else:
        print("Form validation errors:", form.errors)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data in users:
            flash('Username deja folosit!', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(len(users) + 1, form.username.data, hashed_password)
            users[form.username.data] = user
            login_user(user)
            flash('Înregistrare reușită!', 'success')
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Te-ai deconectat cu succes', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
