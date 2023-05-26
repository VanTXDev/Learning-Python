from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "keystone"
app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/")
def hello_world():
	return render_template("home.html") 

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

if __name__ == "__main__":
	app.run(debug=True)