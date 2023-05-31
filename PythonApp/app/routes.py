from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
from app import db

@app.route("/")
def index():
	sql = "SELECT * FROM `todo_list` WHERE del_flag = '' ORDER BY date_created DESC"
	c=db.cursor()
	c.execute(sql)
	result = c.fetchall()
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
def set_complete():
	data = {}
	try:
		isCompleted = bool(request.json['is_completed'])
		taskId = int(request.json['task_id'])

		cur=db.cursor()
		cur.execute("UPDATE todo_list SET is_completed = (%s) WHERE id = (%s)", (isCompleted, taskId))
		db.commit()
		cur.close()
		data = {"status": "true", "is_completed": isCompleted, "task_id": taskId, "message": "Update task status successfully!"}
	except Exception:
		print (Exception)
		data  = {"status": "false", "message": "Update task status failed!"}
	return jsonify(data)

@app.route('/todo/<taskId>', methods=['GET', 'POST'])
def todo_detail(taskId):
	try:
		#Get task informations
		if request.method == 'GET':
			cur=db.cursor()
			cur.execute("SELECT * FROM `todo_list` WHERE id = (%s)", (taskId))
			result = cur.fetchone()
			cur.close()
			return render_template('todo_detail.html', taskDetail=result)
	
		#Update task details
		taskId = request.form['task_id']
		title = request.form['title']
		description = request.form['description']
		is_completed = str(request.form['is_completed'])
		is_completed = bool(is_completed)
		cur=db.cursor()
		cur.execute("UPDATE todo_list SET title = (%s), description = (%s), is_completed = (%s) WHERE id = (%s)", (title, description, is_completed, taskId))
		db.commit()
		cur.close()
	except Exception:
		print (Exception)
	return redirect(url_for("index"))

@app.route("/delete_task", methods=["POST"])
def delete_task():
	data = {}
	try:
		taskId = request.json['task_id']
		cur=db.cursor()
		cur.execute("UPDATE todo_list SET del_flag = 'DEL' WHERE id = (%s)", (taskId))
		db.commit()
		cur.close()
		data = {"status": "true", "message": "Delete task successfully!"}
	except Exception:
		print (Exception)
		data  = {"status": "false", "message": "Delete task failed!"}
	return jsonify(data)