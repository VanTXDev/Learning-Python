from flask import Flask
from datetime import timedelta
from app.conf import SECRET_KEY
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.permanent_session_lifetime = timedelta(minutes=2)

# config mysql connection
db=MySQLdb.connect( host='localhost',
        user='root',
        password='',
        database='todo', cursorclass=MySQLdb.cursors.SSCursor)

from app import routes