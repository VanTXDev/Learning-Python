from flask import render_template, request, redirect, url_for, session
from app import app
from app import db

@app.route("/")
def index():
	sql = "SELECT * FROM `todo_list`"
	c=db.cursor()
	c.execute(sql)
	print (type(c))
	print (c)
	for row in c:
		print (row)
	return render_template("home.html", todoList=c) 

@app.route("/user")
def user():
	if "username" in session:
		return render_template("user.html") 
	else:
		return redirect(url_for("login"))

@app.route("/login", methods=['GET', 'POST'])
def login():
	if "username" in session:
		return redirect(url_for("user"))

	if request.method == 'POST':
		username = request.form['username']
		if username:
			session["username"] = username
			return redirect(url_for("user"))
	return render_template("login.html")

@app.route('/logout')
def logout():
	if "username" in session:
		session.pop("username", None)
		return redirect(url_for("login"))

@app.route('/todo')
def todo():
	return render_template("todo.html")