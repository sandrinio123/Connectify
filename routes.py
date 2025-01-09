from flask import render_template, redirect, url_for, flash
from forms import BlogForm, Register_Form, Login_Form
from flask_login import login_user, logout_user, current_user, login_required
from ext import app, db
from models import Product, User
import os
from datetime import datetime

@app.route('/')
def home():
    blogs = Product.query.all()
    users = {user.id: user for user in User.query.all()}
    print(blogs)
    print(current_user.is_authenticated)
    return render_template('index.html', blogs=blogs, users = users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register_Form()
    if form.validate_on_submit():
        file = form.img.data
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{timestamp}_{file.filename}"
        file.save(os.path.join(app.root_path, "static", "uploads", unique_filename))

        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            password=form.password.data,
            username=form.username.data,
            role='Guest',
            img=unique_filename
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    if not form.validate_on_submit():
        print(form.errors)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user != None and user.check_password(form.password.data):
            login_user(user)
            print(current_user.is_authenticated)
            return redirect(url_for('home'))
        else:
            flash('Password is incorrect')            
    if not form.validate_on_submit():
        print(form.errors)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/delete_blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    if current_user.role != 'admin':
        return redirect("/home")
    
    blog_to_delete = Product.query.get_or_404(blog_id)
    db.session.delete(blog_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/blogs/<int:blog_id>')
def blog_contents(blog_id):
    blog_data = Product.query.get(blog_id)
    users = {user.id: user for user in User.query.all()}
    if blog_data:
        return render_template('blogs.html', blog=blog_data, users=users)
    else:
        return "Blog not found"


@app.route('/profiles')
def profiles():
    users = User.query.all()
    return render_template('profiles.html', users=users)


@app.route('/users/<int:user_id>')
def user_blogs(user_id):
    user_data = User.query.get(user_id)
    all_blogs = Product.query.all()
    user_blogs = [blog for blog in all_blogs if blog.user_id == user_id]
    if user_data:
        return render_template('user_blogs.html', user=user_data, blogs=user_blogs)
    else:
        return "User not found"


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogForm()
    if form.validate_on_submit():  
        contents = Product(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            user_id=current_user.id
        )

        db.session.add(contents)
        db.session.commit()
        return redirect(url_for('home'))
    if not form.validate_on_submit():
        print(form.errors)
    return render_template('create_post.html', form=form)
