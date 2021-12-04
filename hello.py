from datetime import date
import os
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from projectModels import Posts, User, db
from useforms import LoginForm, Post_form, PasswordForm, NameForm, UserForm


# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key for csrf"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.environ.get("USER_NAME")+':'+os.environ.get("PASSWORD")+'@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

# Flask Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/add_posts', methods=['GET', 'POST'])
@login_required
def add_posts():
    form = Post_form()
    if form.validate_on_submit():
        post = Posts(title=form.title.data,
                     content=form.content.data,
                     author=form.author.data,
                     slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash("BlogPost Submit Sucessfully")

    return render_template("add_post.html", form=form)


# Delete Posts
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        # Return A Message
        flash("Blog Post Deleted")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

    except:
        flash("Sorry This Post Not Deleted , We Fix This Soon...")


@app.route('/posts', methods=["GET", "POST"])
@login_required
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


@app.route('/post/<int:id>')
@login_required
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = Post_form()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash("Post Has been updated")

        return redirect(url_for("posts"))

    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content

    return render_template(
        'edit_post.html',
        form=form,
    )


@app.route('/date')
def get_current_date():
    return {"date": date.today()}


# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.password_hash = request.form['password_hash']
        name_to_update.password_hash2 = request.form['password_hash_2']
        try:
            db.session.commit()
            flash("User Update Successfully")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("There Is Problem ")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update)


# Delete Users
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    form = UserForm()
    name = None
    our_users = User.query.order_by(User.date_added)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Sucessfully! ")
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users)

    except:
        print('Got Some error')
        flash('Oops There Is a Problem')
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users)


# create a route Add User
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash The Password
            hashed_password = generate_password_hash(form.password_hash.data,
                                                     "sha256")
            user = User(name=form.name.data,
                        username=form.username.data,
                        email=form.email.data,
                        favorite_color=form.favorite_color.data,
                        password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("User Added Sucessfully.....")
    our_users = User.query.order_by(User.date_added)

    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


# Create a route decorator
@app.route('/')
def index():
    first_name = "Jhon"
    favorite_pizza = ["Chicken", "Peproni", "Cheese", "Mushrooms"]
    return render_template("index.html",
                           name=first_name,
                           favorite_pizza=favorite_pizza)


# localhost:5000/user/kappa
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


# Create a custom  Error Page
# Invalid URL
@app.errorhandler(404)
def page_not_found(Error):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(Error):
    return render_template("500.html"), 500


# Create name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted successfully")

    return render_template("name.html", name=name, form=form)


# Text password
@app.route('/test_pass', methods=['GET', 'POST'])
def test_pass():
    email = None
    password = None
    pass_to_check = None
    passed = None

    form = PasswordForm()

    # validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data = ''

        pass_to_check = User.query.filter_by(email=email).first()
        passed = check_password_hash(pass_to_check.password_hash, password)

        if (passed):
            flash("Password Is Correct")
        else:
            flash("Email or Password Wrong")

        # flash("Form Submitted successfully")

    return render_template("test_password.html",
                           email=email,
                           password=password,
                           pass_to_check=pass_to_check,
                           passed=passed,
                           form=form)


# Create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password - Try again')
        else:
            flash('The user not registered')

    return render_template("login.html", form=form)


# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out >>>>>>>>>>>>')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']

        try:
            db.session.commit()
            flash("User Update Successfully")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("There Is Problem ")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("dashboard.html",
                               form=form,
                               name_to_update=name_to_update, id=id)


if __name__ == '__main__':
    app.run(debug=True)
