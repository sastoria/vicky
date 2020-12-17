import os
import secrets

from PIL import Image  # image resize

from flask import \
    (render_template, send_from_directory, session, request, redirect, url_for, flash, abort)
from flask_login import \
    (login_required, login_user, current_user, logout_user)
from app import (app, db, bcrypt)
from .forms import \
    (RegistrationForm, LoginForm, UpdateForm, CustomerForm)
from app.models import User, Customer
from datetime import timedelta
from imgurpython import ImgurClient
import ENV

# imgur
client_id = ENV.CLIENT_ID
client_secret = ENV.CLIENT_SECRET
access_token = ENV.ACCESS_TOKEN
refresh_token = ENV.REFRESH_TOKEN
client = ImgurClient(client_id, client_secret, access_token, refresh_token)


@app.route("/robots.txt")
def robots(): return send_from_directory(app.static_folder, "robots.txt")


@app.route('/', methods=["POST", "GET"])
def index(): return render_template('index.html', title='Home Page')


@app.route('/about', methods=["POST", "GET"])
def about():
    return render_template('about.html', title='About Vicky')


def save_picture(form_picture):
    size = (125, 125)
    resize = Image.open(form_picture).thumbnail(size)
    filename = secrets.token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    image = filename + ext
    store_path = os.path.join(app.root_path, 'static/image ', image)
    resize.save(store_path)
    return image


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image = save_picture(form.picture.data)
            current_user.image = image
        current_user.username = form.username.data
        # current_user.email = form.email.data
        db.session.commit()
        flash('Update complete', 'success')
        return redirect(url_for('account'))
    image = url_for('static', filename=f'image/{current_user.profile}')
    data = {'title': 'Account', 'form': form, 'image': image}
    return render_template('login.html', **data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data, 12).decode('utf-8')
        user = User(name=form.name.data, account=form.account.data,
                    email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Registration Successful [ {form.account.data } ]', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('index'))
    form = LoginForm()
    session.permanent = True  #  set session alive time
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data, duration=timedelta(days=7))  #
            flash(f'Welcome back , {user.account}', 'success')
            next_page = request.args.get('next')
            """because 'next' is optional,so use .get() rather than [] to avoid error that can't find the dict value"""
            return redirect(next_page) if next_page else redirect(url_for('index'))
            #
            # return redirect(next_page or url_for('adim'))
        else:
            flash(f"Please check your email and password", 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out', 'info')
    return redirect(url_for('login'))

# todo need to get the idea


def searching_engine(form):
    query = form
    pass


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    event = ['search', 'delete', 'update', 'create']
    if event in searching_engine:
        pass
    pass
    form = None
    return render_template('search.html', form=form, title='Search')


# Create route-------------------------------------------------------------


@app.route('/create')
@login_required
def create():

    return render_template('creator/create.html', title='Create')


@app.route('/create/add-customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(name=form.name.data, contact=form.contact.data,
                            gender=form.gender.data, birthday=form.birthday.data,
                            remark=form.remark.data, user_id=current_user.id)
        db.session.add(customer)
        db.session.commit()
        flash('Object has been created', 'warning')
        return redirect(url_for('add_customer'))
    return render_template('creator/add-customer.html', form=form, title='Add Customer')


@app.route('/create/add-tag', methods=['GET', 'POST'])
@login_required
def add_tag():
    return render_template('creator/add-tag.html')