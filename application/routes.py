from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Posts, Users
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user,current_user, logout_user, login_required
from application.functions import s3download_file, s3upload_file
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileRequired
import os 

@app.route('/')
@app.route('/home')
def home():

    postData = Posts.query.all() 
    return render_template('home.html', title='Home', posts=postData)
    

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        f = form.photo.data
        save_photo = save_photo(f)
        if save_photo:
            print ("ffffffffffffffffffffffffffffffffffffffff")
            print (f)
            image_name = f

            postData = Posts(
                    title = form.title.data,
                    content = form.content.data,
                    author = current_user,
                    image_name = image_name
                    #image_url = image_url

            )
            db.session.add(postData)
            db.session.commit()
        
            return redirect(url_for('home'))
        else:
            print ("Photo could not save")
    else:
        print(form.errors)
    
    return render_template('post.html', title='Post', form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            first_name=form.first_name.data,
            last_name = form.last_name.data,
            email=form.email.data,
            password=hashed_pw
            )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('post'))
    return render_template('register.html',title='Register',form=form)
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password,
         form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else: 
            
                return redirect(url_for('home'))
    
    return render_template('login.html', title='login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)