# from the flask library import a class named Flask
from flask import Flask, render_template, request

# create an instance of the Flask class
app = Flask(__name__)

# listen for a route to `/` - this is known as the root route
@app.route('/')
# when this route is reached (through the browser bar or someone clicking a link, run the following function)
def hello():
    names = ["Ha", "Hoa", "Hiep"]
    # this `return` is the response from our server. We are responding with the text "Hello World"
    # return "Hello World.!"
    return render_template('index.html', names=names)

@app.route('/hi')
def hi():
    return "Hi!"

@app.route('/bye')
def bye():
    return "Bye!"

# list dynamic routing with string
@app.route('/name/<person>')
def say_name(person):
    return f"The name is {person}"

# list dynamic routing with number
@app.route('/name/<int:num>')
def say_num(num):
    return f"The number is {num}"

# extends template from base.html template
@app.route('/template')
def title():
    return render_template("title.html")

# getting data from a form
# rendering a form
@app.route('/show')
def show_form():
    return render_template("first-form.html")

# form submitting
@app.route('/data')
def data():
    first = request.args.get("first")
    last = request.args.get("last")
    return f"You put {first} {last}"