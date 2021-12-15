from app import app
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
def index():

    return render_template('index.html',title='WELCOME')



@app.route('/my-interviews')
@login_required
def interviews():

    return render_template('interviews.html',title='My Interviews')

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_parse('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        flash('Login requested for user {} remember me is {}'.format(form.username.data,form.remember_me.data))
        return redirect(next_page)
    
    return render_template('login.html',title='Sign In',form=form)
