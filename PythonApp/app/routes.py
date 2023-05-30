from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
from app import db

@app.route("/")
def index():
	sql = "SELECT * FROM `todo_list`"
	c=db.cursor()
	c.execute(sql)
	result = c.fetchall()
	print (type(result))
	print (result)
	for row in result:
		print (row)
	return render_template("home.html", todoList=result) 

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

@app.route('/todo', methods=['GET', 'POST'])
def todo():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form['description']
		is_completed = '0'

		cur=db.cursor()
		cur.execute("INSERT INTO todo_list(title, description, is_completed) VALUES (%s, %s, %s)", (title, description, is_completed))
		db.commit()
		cur.close()
		return redirect(url_for("index"))
	return render_template("todo.html")

@app.route('/set_complete', methods=['POST'])
def set_completed():
	print("Setting completed: " + request.get_json())
	data = {"hello": "world"}
	return jsonify(data)