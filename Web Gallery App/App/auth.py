from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash




auth = Blueprint('auth', __name__)


#Route to direct to log in page 
@auth.route('/')
def go_to_login():

    return redirect(url_for('auth.login'))

#Page for logging in
@auth.route('/login', methods =['GET', 'POST'])
def login():

    if(request.method == 'POST'):

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if(user):

            if(check_password_hash(user.password,  password)):
                flash(f'Welcome to WebGal {user.first_name}', category='success')
                login_user(user)
                return redirect(url_for('views.dashboard'))
            else:
                flash('This password is incorrect', category='error')

        else:

            flash('This user does not exist', category='error')



    return render_template('login.html', user = current_user)

#Page for user registration
@auth.route('/register-account', methods =['GET', 'POST'])
def register():

    if(request.method == 'POST'):

        #Get the user data
        first_name = request.form.get('first-name')
        second_name = request.form.get('second-name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_comfirm = request.form.get('password-confirm')

        #Check for errors

        user = User.query.filter_by(email = email).first()

        if(user):
            flash('This email already exists, try another one', category='error')
        
        elif len(first_name) < 2 or len(second_name) < 2:
            flash('The name fields should not be empty or less than two characters',
            category='error')

        elif( len(password) < 7):
            flash('The password should be atleast 7 characters wide',  category='error')

        elif( password != password_comfirm):
            flash('Make sure that you comfirm the password correctly', category = "error")
        
        else:

            new_account = User(first_name = first_name,
                                second_name = second_name,
                                email = email,
                                password = generate_password_hash(password, 'sha256'))
            db.session.add(new_account)
            db.session.commit()
            flash(f'Welcome to WebGal {new_account.first_name}' , category='success')
            login_user(new_account)
            return redirect(url_for('views.dashboard'))



    
    return render_template('register.html', user = current_user)