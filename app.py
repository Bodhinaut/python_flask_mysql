from flask import Flask, render_template, request
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import yaml
app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml') )
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


# mysql = MySQL(app)
mysql = MySQL()
mysql.init_app(app)

# now need to add routes to server so no 404
@app.route('/', methods=['GET', 'POST']) # have url take post request
def index():
	# check what request is 
	if request.method == 'POST':
		# Fetch form data
		userDetails = request.form
		name = userDetails['name']
		email = userDetails['email']
		#cur = mysql.connection.cursor() # execute queries
		cur = mysql.get_db().cursor()
		cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email) )
		mysql.connection.commit()
		cur.close()
		return 'Success'
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True) # debug on for constant updates without restart
