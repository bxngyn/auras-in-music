import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# citation: CS50 Finance PSet
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configuring shortened sqlite commands
db = SQL("sqlite:///static/auras.db")
db_nostalgic = SQL("sqlite:///static/nostalgicsongs.db")
db_sad = SQL("sqlite:///static/sadhour.db")
db_happy = SQL("sqlite:///static/happyvibe.db")
db_ok = SQL("sqlite:///static/indiesongs.db")

# citation: CS50 Finance PSet
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Main page"""

    # store current user's id
    user_id = session["user_id"]

    # select all attributes of the current user
    usernames = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    return render_template("layout.html", usernames=usernames)

# citation: my CS50 Finance PSet
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        # no first name submission
        if not request.form.get("first_name"):
            return apology("Missing first name.")
        # no username submission
        if not request.form.get("username"):
            return apology("Missing username.")
        # no password submission
        elif not request.form.get("password"):
            return apology("Missing password.")
        # no confirmation submission
        elif not request.form.get("confirmation"):
            return apology("Please confirm your password.")
        # no password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")
        # query users for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # check username
        if len(rows) == 1:
            return apology("Username has already been taken.")
        # hash password
        hash = generate_password_hash(request.form.get("password"))
        # insert newly registered user into database
        user = db.execute("INSERT INTO users (username, hash, first_name) VALUES(?, ?, ?)", request.form.get("username"), hash, request.form.get("first_name"))

        session["user_id"] = user

        return redirect("/")

    else:
        return render_template("register.html")

# citation: my CS50 Finance PSet
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# citation: my CS50 Finance PSet
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/auras")
@login_required
def auras():
    """Open aura page"""
    user_id = session["user_id"]
    usernames = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    return render_template("auras.html", usernames=usernames)

@app.route("/history")
@login_required
def history():
    """History page of user"""

    # keep track of user id
    user_id = session["user_id"]

    # gather data on user's transactions and store into variable
    history = db.execute("SELECT song, artist, type, time FROM history WHERE user_id = ?", user_id)

    return render_template("history.html", history=history)


@app.route("/nostalgic", methods=["GET", "POST"])
@login_required
def nostalgic():
    """ Runs when nostalgic button is pressed """

    if request.method == "POST":
        # I used this link since I didn't know what the syntax was for randomly selecting out of a table using SQL. https://stackoverflow.com/questions/580639/how-to-randomly-select-rows-in-sql
        # source of nostalgic song database: https://www.kaggle.com/datasets/leonardopena/top-spotify-songs-from-20102019-by-year?resource=download

        # select name and artist of top songs from 2010-2012
        nostalgic_song = db_nostalgic.execute("SELECT title, artist FROM top10s WHERE year = 2010 OR year = 2011 OR year = 2012 ORDER BY RANDOM() LIMIT 1;")

        # store current user's id
        user_id = session["user_id"]

        # insert into history table the song/artist the user got as well as the emotion they pressed
        db.execute("INSERT INTO history (user_id, song, artist, type) VALUES (?, ?, ?, ?)", user_id, nostalgic_song[0]['title'], nostalgic_song[0]['artist'], 'nostalgic')

        return render_template("result.html", nostalgic_song=nostalgic_song)

    else:
        return redirect("/")

@app.route("/sad", methods=["GET", "POST"])
@login_required
def sadhour():
    """ Runs when sad button is pressed """
    # I couldn't find a database I liked, so I made my own with these two playlists: https://open.spotify.com/playlist/64SdJH0YGxfOBhHV533bPC?si=1069d54e66b84de8 and https://open.spotify.com/playlist/37i9dQZF1DWSqBruwoIXkA?si=5943267c3e1a4b06
    # I used https://exportify.net/ to convert Spotify playlists into CSV files
    # I used https://sqlizer.io/ to convert CSV file into SQL file
    if request.method == "POST":

        # select name and artist of song from sad song database
        sad_song = db_sad.execute("SELECT track_name, artist_name_s FROM sad_hour ORDER BY RANDOM() LIMIT 1;")

        # store current user's id
        user_id = session["user_id"]

        # insert into history table the song/artist the user got as well as the emotion they pressed
        db.execute("INSERT INTO history (user_id, song, artist, type) VALUES (?, ?, ?, ?)", user_id, sad_song[0]['Track_Name'], sad_song[0]['Artist_Name_s'], 'sad')

        return render_template("result.html", sad_song=sad_song)

    else:
        return redirect("/")

@app.route("/happy", methods=["GET", "POST"])
@login_required
def happyvibes():
    """Runs when happy button is pressed"""
    # I made a database using this Spotify playlist: https://open.spotify.com/playlist/3rTliUjFBUwKukZLH15tkE?si=fcee4994e704408d.
    if request.method == "POST":

        # select name and artist of song from happy song database
        happy_song = db_happy.execute("SELECT track_name, artist_name_s FROM happy_vibes ORDER BY RANDOM() LIMIT 1;")

        # store current user's id
        user_id = session["user_id"]

        # insert into history table the song/artist the user got as well as the emotion they pressed
        db.execute("INSERT INTO history (user_id, song, artist, type) VALUES (?, ?, ?, ?)", user_id, happy_song[0]['Track_Name'], happy_song[0]['Artist_Name_s'], 'happy')

        return render_template("result.html", happy_song=happy_song)

    else:
        return redirect("/")

@app.route("/justok", methods=["GET", "POST"])
@login_required
def justok():
    """Runs when just ok button is pressed"""
    
    # I made a database using this Spotify playlist: https://open.spotify.com/playlist/37i9dQZF1DX26DKvjp0s9M?si=ddb1001340b44507
    if request.method == "POST":

        # select name and artist of song from database that has mostly indie songs
        ok_song = db_ok.execute("SELECT track_name, artist_name_s FROM essential_indie ORDER BY RANDOM() LIMIT 1;")

        # store current user's id
        user_id = session["user_id"]

        # insert into history table the song/artist the user got as well as the emotion they pressed
        db.execute("INSERT INTO history (user_id, song, artist, type) VALUES (?, ?, ?, ?)", user_id, ok_song[0]['Track_Name'], ok_song[0]['Artist_Name_s'], 'just ok')

        return render_template("result.html", ok_song=ok_song)

    else:
        return redirect("/")

