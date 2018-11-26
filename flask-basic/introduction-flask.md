# Objectives
- Install pyenv and create virtual environments
- Use Flask to set up a simple server and respond with text

## Install pyenv
1. CentOS
	- curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
	- setup `.bash_profiles`
		```
		export PATH="~/.pyenv/bin:$PATH"
		eval "$(pyenv init -)"
		eval "$(pyenv virtualenv-init -)"
		```
2. Using pyenv
	- `pyenv versions`
	- `pyenv global`
	- `pyenv install 3.6.0`
	- `pyenv update`
	- `pyenv install --list`
	- `pyenv uninstall [-f|--force] <version>`
3. Create python virtual enviroments
	- `python -m venv py_venv`
	- `source py_venv/bin/activate`
	- `pip install --upgrade pip`
4. Install Flask framework
	- `pip install flask`
## Setup Flask
### Flask Introduction
1. Create `app.py`
	```
	# from the flask library import a class named Flask
	from flask import Flask
	
	# create an instance of the Flask class
	app = Flask(__name__)
	
	# listen for a route to `/` - this is known as the root route
	@app.route('/')
	# when this route is reached (through the browser bar or someone clicking a link, run the following function)
	def hello():
	    # this `return` is the response from our server. We are responding with the text "Hello World"
	    return "Hello World!"
	```
2. Running flask
	- `export FLASK_APP=app.py`
	- `flask run`
	- Access to http://127.0.0.1:5000 => getting `Hello World!` text
3. Running flask in debug mode => auto reload app if make any changes
	- `export FLASK_APP=app.py`
	- `export FLASK_DEBUG=1`
	- `flask run`
	- Access to http://127.0.0.1:5000 => getting `Hello World!` text
### Routing with Flask
- Create multiple routes with Flask
- Capture URL parameters and define their types
1. Let's make an app.py file with routing `/, /hi, /bye`
	```
	from flask import Flask
	
	app = Flask(__name__)
	
	@app.route('/')
	def hello():
	    return "Hello!"
	
	@app.route('/hi')
	def hi():
	    return "Hi!"
	
	@app.route('/bye')
	def bye():
	    return "Bye!"
	```
2. Running flask in debug mode => auto reload app if make any changes
	- `export FLASK_APP=app.py`
	- `export FLASK_DEBUG=1`
	- `flask run`
	- Access to http://127.0.0.1:5000 => getting `Hello` text
	- Access to http://127.0.0.1:5000/hi => getting `Hi!` text
	- Access to http://127.0.0.1:5000/bye => getting `Bye!` text
3. We can create a URL parameter using <NAME_OF_VARIABLE> in our route
	```
	#let's make up a parameter called name. Its value is going to be WHATEVER someone requests, but we will respond with the string "The name is" along with the value in the URL.
	@app.route('/name/<person>')
	def say_name(person):
	    return f"The name is {person}"
	
	# since all URL parameters are strings, we can convert them right away to another data type in our route definition
	@app.route('/name/<int:num>')
	def favorite_number(num):
	    return f"Your favorite number is {num}, which is half of {num * 2}"
	```
### Templating with Jinja2
- Use Flask to respond by rendering HTML instead of plain text
- Use Jinja2 as a server side templating engine
- Pass values to a server side template with Flask and evaluate them with Jinja
1. Jinja2 syntax
	- We use the `{% %}` notation
	- We use `{{ }}` to print data
2. Rendering HTML. We must include render_template from Flask
	```
	from flask import Flask, render_template # we are now importing just more than Flask!
	
	app = Flask(__name__)
	
	@app.route('/')
	def welcome():
	    names_of_instructors = ["Elie", "Tim", "Matt"]
	    random_name = "Tom"
	    return render_template('index.html', names=names_of_instructors, name=random_name)
	
	@app.route('/second')
	def second():
	    return "WELCOME TO THE SECOND PAGE!"
	```
	- Create 'templates' folder for render_templates and create `index.html' inside `templates` folder
	```
		code
		├── app.py
		└── templates
		    └── index.html
	```
3. Template Inheritance
	- which means that one template can inherit from another
	- We use `extends` keyword to inherit from other templates
	- Example
		+ Create a file called `base.html`
		```
			<!DOCTYPE html>
			<html lang="en">
			<head>
			    <meta charset="UTF-8">
			    <title>Document</title>
			</head>
			<body>
			   {% block content %}
			   {% endblock %}
			</body>
			</html>
		```
		+ Create a file called title.html in the same directory
		```
			{% extends "base.html" %}
			{% block content %}
				<h1>This page has everything our base.html has!</h1>
			{% endblock %}
		```
		+ Folder structure
		```
			code
			├── app.py
			└── templates
			    ├── base.html
			    ├── index.html
			    └── title.html			
		```
4. Using `url_for` helper which eliminates the need for hard coding a URL
	```
	{% extends "base.html" %}
	{% block content %}
	Head over to <a href="{{url_for('hi')}}">the second page!</a>
	{% endblock %}
	```
5. Getting data from the query string by using `request` keyword with it's `args` attributes
	- Create `first-form.html` in `templates` folder
		```
		{% extends "base.html" %}
		{% block content %}
		    <form action="/data">
		        <input type="text" name="first">
		        <input type="text" name="last">
		        <input type="submit" value="Submit Form">
		    </form>
		{% endblock %}
		```
	- edit `app.py` with content
		```
		from flask import Flask, render_template, request
	
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
		```
	- Folder structure
		```
		code
		├── app.py
		└── templates
		    ├── base.html
		    ├── first-form.html
		    ├── index.html
		    └── title.html
		```
6. Macros
	- we can use macros to abstract commonly used code snippets that are used over and over to not repeat ourselves
	- Example
		+ Create `macros.html` in `templates` folder
		```
			{% macro nav_link(endpoint, name) %}
			{% if request.endpoint.endswith(endpoint) %}
			  <li class="active"><a href="{{ url_for(endpoint) }}">{{name}}</a></li>
			{% else %}
			  <li><a href="{{ url_for(endpoint) }}">{{name}}</a></li>
			{% endif %}
			{% endmacro %}
		```
		+ update `base.html` with content and navigate to `/show` or `template` routes
		```
			{% from "macros.html" import nav_link with context %}
			...
			<body>
				<ul class="nav navbar-nav">
		        	{{ nav_link('title', 'Template') }}
			        {{ nav_link('show_form', 'Show') }}
			    </ul>
			</body>
		```
		+ Folder structure
		```
			code
			├── app.py
			└── templates
			    ├── base.html
			    ├── first-form.html
			    ├── index.html
			    ├── macros.html
			    └── title.html
		```
9. [Refer link](https://realpython.com/blog/python/primer-on-jinja-templating/)
### [Flask with CRUD](https://www.rithmschool.com/courses/flask-fundamentals/crud-with-flask)
- GET `/students` -> render a page called 'index.html' (typically with information on all students)
- GET `/students/new` -> render a page called 'new.html' (typically with a form to create a new student)
- GET `/students/:id` -> render a page called 'show.html' (typically with information on the student with the given id)
- GET `/students/:id/edit` -> render a page called 'edit.html' (typically with a form to edit the student with the given id)
- POST `/students` -> create a new resource, then redirect
- PATCH `/students/:id` -> find a resource by the id, update it, then redirect
- DELETE `/students/:id` -> find a resource by the id, remove it, then redirect