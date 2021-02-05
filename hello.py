from flask import Flask,render_template

# Create a Flask Instance
app = Flask(__name__)


 # create a route

 # Create a route decorator
@app.route('/')

def index():
	first_name = "Jhon"
	favorite_pizza =["Chicken","Peproni","Cheese","Mushrooms"]
	return render_template("index.html",name=first_name,favorite_pizza=favorite_pizza)


# localhost:5000/user/kappa
@app.route('/user/<name>')
def user(name):
	return render_template("user.html",user_name=name)

# Create a custom  Error Page

#Invalid URL
@app.errorhandler(404)
def page_not_found(Error):
	return render_template("404.html"),404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(Error):
	return render_template("500.html"),500
	

if __name__ == '__main__':
	app.run(debug=True)