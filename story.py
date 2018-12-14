# Import outside tools
from random import randint, shuffle
from cs50 import SQL

# Configure application, templates, database and arrays
data = SQL("sqlite:///story.db")
elements = ["character", "aspect", "place", "thing", "event", "ending"]

# For each element type
for element in elements:

    # Get element set from database based on preferences and shuffle
    deck = data.execute("SELECT name FROM elements WHERE type = :type", type=element)
    shuffle(deck)

    # Pick one random element and print
    pick = randint(1, len(deck))
    print(element + ": " + deck[pick]["name"])

# Get stages set from database and shuffle
deck = data.execute("SELECT name, description FROM stages")
shuffle(deck)
stages = set()

# Pick five stages at random and print
while len(stages) < 5:
    stages.add(randint(1, len(deck)))
stages = list(stages)
shuffle(stages)

for i in stages:
    print(deck[i]["name"] + " - " + deck[i]["description"])
