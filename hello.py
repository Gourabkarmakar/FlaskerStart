from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from text import user_name,password
import text
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key for csrf"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + text.user_name + ':' + text.password + '@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Model

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String(255))

class Post_form(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget= TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.now)

    # Password section
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password Is Not a readable attribuite')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField("Password",
                                  validators=[
                                      DataRequired(),
                                      EqualTo('password_hash2',
                                              message="Passwords Must Match! ")
                                  ])
    password_hash2 = PasswordField("Confirm Password",
                                   validators=[DataRequired()])
    submit = SubmitField('Submit')


class NameForm(FlaskForm):
    name = StringField("What Is Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordForm(FlaskForm):
    email = StringField("What is your Email", validators=[DataRequired()])
    password_hash = PasswordField("What is Your Passwords",validators=[DataRequired()])
    submit = SubmitField("Check")



@app.route('/add_posts', methods=['GET', 'POST'])
def add_posts():
    form = Post_form()
    if form.validate_on_submit():
        post = Posts(
            title = form.title.data,
            content = form.content.data,
            author = form.author.data,
            slug = form.slug.data)
        form.title.data= ''
        form.content.data= ''
        form.author.data= ''
        form.slug.data=''

        db.session.add(post)
        db.session.commit()

        flash("BlogPost Submit Sucessfully")

    return render_template("add_post.html",form= form)

# Delete Posts
@app.route('/posts/delete/<int:id>')
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
        

@app.route('/posts', methods=["GET","POST"])
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/post/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template(
        'post.html',post=post)

@app.route('/posts/edit_post/<int:id>', methods=['GET','POST'])
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
        form = form,
    )



@app.route('/date')
def get_current_date():
    return{"date": date.today()}


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
        name_to_update.password_hash2= request.form['password_hash_2']
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
                        email=form.email.data,
                        favorite_color=form.favorite_color.data,
                        password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
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
    passed= None

    form = PasswordForm()

    # validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data= ''

        pass_to_check = User.query.filter_by(email=email).first()
        passed = check_password_hash(pass_to_check.password_hash, password)

        if(passed):
            flash("Password Is Correct")
        else:
            flash("Email or Password Wrong")

        # flash("Form Submitted successfully")

    return render_template("test_password.html",email=email,
    password=password,pass_to_check=pass_to_check,passed=passed,form=form)


if __name__ == '__main__':
    app.run(debug=True)
