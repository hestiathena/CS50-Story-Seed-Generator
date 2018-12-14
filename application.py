# Final Project for CS50x - Story Seed Generator By Elanore Hall (Hestiathena) August 2018
# Inspired by the Once Upon a Time card game, created by Richard Lambert, Andrew Rilstone and James Wallis, Published by Atlas Games
# And the Once Upon a Time Writer's Handbook, Written by Kelly Olmstead

# Import outside tools
from random import randint, shuffle
from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application and set automatic reload
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Do not cache the pages
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Initialize database and element array
data = SQL("sqlite:///story.db")
elements = ["character", "aspect", "place", "thing", "event", "ending"]
genre = ["Adventure", "Fantasy", "Scifi", "Mystery", "Horror", "Romance"]


@app.route("/", methods=["GET", "POST"])
def index():

    # User reached page via GET, display instructions and options
    if request.method == "GET":
        return render_template("index.html")

    # User reached page via POST, run program core and display results
    elif request.method == "POST":

        # Store the form data, if any
        # (There's got to be a more elegant way to do this...)
        formdata = dict()

        if request.form.get("multiple"):
            formdata["multiple"] = request.form.get("multiple")
        if request.form.get("twocharacter"):
            formdata["twochar"] = request.form.get("twochar")
        if request.form.get("twoaspect"):
            formdata["twoasp"] = request.form.get("twoasp")
        if request.form.get("twoplace"):
            formdata["twoplace"] = request.form.get("twoplace")
        if request.form.get("twothing"):
            formdata["twothing"] = request.form.get("twothing")
        if request.form.get("twoevent"):
            formdata["twoevent"] = request.form.get("twoevent")
        if request.form.get("genre"):
            formdata["genre"] = request.form.get("genre")

        # For each requested set of data
        results = list()
        for i in range(int(request.form.get("multiple"))):
            sub = dict()

            # For each element type
            for element in elements:

                # Get element set from database based on preferences and shuffle
                deck = data.execute("SELECT name FROM elements WHERE type = :type", type=element)
                shuffle(deck)

                # Pick one random element and add to dict
                sub[element + "1"] = deck[randint(0, len(deck)-1)]["name"]

                # If the user has requested two elements, add an extra
                if request.form.get("two" + element):
                    sub[element + "2"] = deck[randint(0, len(deck)-1)]["name"]

            # Get stages set from database and shuffle
            deck = data.execute("SELECT name, description FROM stages")
            shuffle(deck)

            # Pick five stages at random with no duplicates and add to dict
            stages = set()

            while len(stages) < 5:
                stages.add(randint(0, len(deck)-1))
            stages = list(stages)
            shuffle(stages)

            j = 0
            for i in stages:
                j += 1
                sub["stage" + str(j)] = dict([("name", deck[j]["name"]),
                                             ("description", deck[j]["description"])])

            # Pick a genre and add it to results
            if request.form.get("genre"):
                shuffle(genre)
                sub["genre"] = genre[randint(0, len(genre)-1)]

            # Add completed subresults to main datalist
            results.append(sub)

        # Send data to page for display
        return render_template("index.html", data=results, form=formdata)