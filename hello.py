from flask import Flask, render_template, flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from text import user_name,password 
import text



# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key for csrf"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+text.user_name+':'+text.password+'@localhost/users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Create Model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Submit')


class NameForm(FlaskForm):
    name = StringField("What Is Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

# Update Database Record
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form= UserForm()
    name_to_update= User.query.get_or_404(id)
    if request.method =="POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Update Sucessfully")
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

            
# create a route
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Sucessfully.....")
    our_users = User.query.order_by(User.date_added)

    return render_template('add_user.html', form=form, name=name, our_users=our_users)


# Create a route decorator
@app.route('/')
def index():
    first_name = "Jhon"
    favorite_pizza = ["Chicken", "Peproni", "Cheese", "Mushrooms"]
    return render_template("index.html", name=first_name, favorite_pizza=favorite_pizza)


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

    return render_template("name.html",
                           name=name,
                           form=form)


if __name__ == '__main__':
    app.run(debug=True)
