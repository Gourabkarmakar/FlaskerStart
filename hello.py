from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key for csrf"


# Create a Form Class
class NameForm(FlaskForm):
    name = StringField("What Is Your Name", validators=[DataRequired()])
    submit = SubmitField('Submit')


# create a route

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
