from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "loti_slepeni_123"

@app.before_request
def gatekeeper():
    # Saraksts ar ceļiem, kuriem var piekļūt bez ielogošanās
    # Jāpārbauda savi funkciju (funkciju, nevis path) nosaukumi!
    publiskie_celi = ['sakums', 'login', 'register', 'static']
    
    # Ja lietotājs nav sesijā un mēģina piekļūt ne-publiskam ceļam
    if 'id' not in session and request.endpoint not in publiskie_celi:
        return redirect("/pieteikties")



@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		lietotajs = request.form.get('lietotajs')
		parole = request.form.get('parole')

		conn = sqlite3.connect("imdb2026.db")
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		c.execute("SELECT * FROM lietotaji WHERE lietotajvards = ?", (lietotajs,))
		atbilde = c.fetchone()
		conn.close()

		if atbilde and check_password_hash(atbilde['parole'], parole):
			session["id"] = atbilde["id"]
			session["lietotajs"] = atbilde["lietotajvards"]
			session["vards"] = atbilde["vards"]
			session["tema"] = 'light'
			return redirect("/")
		else:
			return "Nepareizi dati!"

	return render_template("login.html")

@app.route("/game")
def sakums():
	return render_template("game.html")

@app.route("/")
def sakums():
	return render_template("index.html")


if __name__ == "__main__":
	app.run(debug = True)