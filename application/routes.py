from flask import render_template, redirect, url_for
from application import app, db, bcrypt
from application.models import Posts, Users
from application.forms import PostForm, RegistrationForm


@app.route('/')
@app.route('/home')
def home():
    postData = Posts.query.all() 
    return render_template('home.html', title='Home', posts=postData)
    
@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/post', methods=['GET','POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                title = form.title.data,
                content = form.content.data
        )
        
        db.session.add(postData)
        db.session.commit()
    
        return redirect(url_for('home'))
    else:
        print(form.errors)
    
    return render_template('post.html', title='Post', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data.decode('utf-8'))
        user = Users(email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit
        return redirect(url_for('post'))
    return render_template('register.html',title='Register',form=form)

