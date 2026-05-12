
from flask import Flask, render_template, request, redirect, url_for
import sqlite3, random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def datubaze():
	conn = sqlite3.connect('projekts.db')
	c = conn.cursor()
	conn.commit()
	conn.close()

	datubaze()


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		conn = sqlite3.connect('projekts.db')
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		c.execute("SELECT * FROM lietotajs WHERE username=?", (username,))
		user = c.fetchone()

		conn.close()

		if user and check_password_hash(user["password"], password):
			return redirect(url_for('game'))
		else:
			return "Incorrect data"

	return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		conn = sqlite3.connect('projekts.db')
		c = conn.cursor()
		eksiste = c.execute("SELECT * FROM lietotajs WHERE username = ?", (username,)).fetchone()

		if eksiste:
			conn.close()
			flash(f"{username} ir jau aiznemts, megini citu!")
			return redirect(url_for('register.html'))

		password_hash = generate_password_hash(password)

		c.execute("INSERT INTO lietotajs (username, email, password) VALUES (?, ?, ?)", (username, email, password_hash))

		conn.commit()
		conn.close()
		

		return redirect(url_for('game'))

	return render_template('register.html')


@app.route('/game')
def game():
	guesses = []
	keys = []
	for i in range(4):
		dig = random.randrange(0, 10)
		guesses.append(dig)
		if request.method == 'POST':
			digit1 = request.form['input1']
			digit2 = request.form['input2']
			digit3 = request.form['input3']
			digit4 = request.form['input4']
			for one in range(4):
				if digit1 == guesses[0]:
					keys.append(2)
				elif digit2 == guesses[1]:
					keys.append(2)
				elif digit3 == guesses[2]:
					keys.append(2)
				elif digit4 == guesses[3]:
					keys.append(2)
				else:
					keys.append(1)
					   

	return render_template('game.html')

	
@app.route("/stats", methods=['GET', 'POST'])
def stats():
	if request.method == 'POST':
		conn = sqlite3.connect('projekts.db')
		c = conn.cursor()
		users = c.execute("SELECT * FROM lietotajs WHERE username = ?", (username,)).fetchone()

		conn.close()
	darbu_saraksts = [
	{"nosaukums": "uzstādīt Flask", "ilgums": 10, "statuss": True},
	{"nosaukums": "izveidot app.py", "ilgums": 20, "statuss": True},
	{"nosaukums": "pielikt bootstrap", "ilgums": 15, "statuss": False},
	{"nosaukums": "pielikt ievades formas", "ilgums": 30, "statuss": False}
	]

	return render_template("stats.html", darbi = darbu_saraksts)




if __name__ == '__main__':
	app.run(debug=True)