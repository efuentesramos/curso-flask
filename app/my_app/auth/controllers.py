from flask import g, Blueprint, flash, redirect,url_for, render_template

from flask_login import current_user, login_user, logout_user, login_required

from my_app import login_manager,db
from my_app.auth.models import User

from my_app.auth.form import RegistrationForm, LoginForm

authRoute = Blueprint('auth', __name__,)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@authRoute.before_request
def get_current_user():
    g.user =current_user

@authRoute.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('Your are alredy logged in.','info')
        return redirect(url_for('task.index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            print('#####--- este es el usuario existente : ',existing_username)
            flash('This username has been already taken. Try another one','warning')
            return render_template('user/register.html',form=form)
        
        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()

        flash('You are now register. Please Login','success')

        if form.errors:
            flash(form.errors,'danger')

    return render_template('user/register.html',form=form)
        

#---------------

@authRoute.route('/login', methods=['GET','POST'])
def login_u():
    if current_user.is_authenticated:
        flash('Your are alredy logged in.','info')
        return redirect(url_for('task.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            if   existing_username.check_password(password):
                login_user(existing_username)
                flash('You are login now!.','info')
                return redirect(url_for('task.index'))
            
            flash('Your password is wrong!.','info')
            render_template('user/login.html',form=form)
        

        flash('You are not registered on System. Please Register','info')

        

        if form.errors:
            flash(form.errors,'danger')

        return redirect(url_for('auth.register'))
        #return render_template('user/register.html',form=form)

    return render_template('user/login.html',form=form)



@authRoute.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_u'))
        