import requests
import pycountry
import sqlite3
from datetime import datetime

con = sqlite3.connect("games.db", isolation_level=None)
cursor = con.cursor()

# Insert your own Client ID and Authorization key at every API call, fields are left blank.

def gamesearch(game_title):
    response = requests.post(
        "https://api.igdb.com/v4/games",
        **{
            "headers": {
                "Client-ID": "",
                "Authorization": "",
            },
            "data": f'fields id, name, involved_companies, first_release_date, genres; where name ~ "{game_title}"; sort rating desc;',
        },
    ).json()
    return response # returns an array with 1+ games

def publishersearch(response): # returns the publisher name for the first game on the list
    publisher = response[0]["involved_companies"]
    while True:
        for company in publisher:
            is_publisher = requests.post(
                "https://api.igdb.com/v4/involved_companies",
                **{
                    "headers": {
                        "Client-ID": "",
                        "Authorization": "",
                    },
                    "data": f"fields company, publisher; where id = {company};",
                },
            ).json()
            if is_publisher[0]["publisher"]:
                company_name = requests.post(
                    "https://api.igdb.com/v4/companies",
                    **{
                        "headers": {
                            "Client-ID": "",
                            "Authorization": "",
                        },
                        "data": f"fields name, country; where id = {is_publisher[0]['company']};",
                    },
                ).json()
                if company_name == "":
                    return "None"
                else:
                    return company_name


# retrieve game information from API
game_info = gamesearch(input("Game: "))
publisher_info = publishersearch(game_info)
# checkduplicates(game_info, publisher_info)

# setting up game information
rating = int(input("Your rating: "))
name = game_info[0]["name"]
publisher_name = publisher_info[0]["name"]
release_date = datetime.fromtimestamp(game_info[0]["first_release_date"]).strftime("%Y-%m-%d")

if game_info[0]["id"] > 65535:
    gameid = int(game_info[0]["id"]) % 65535
else:
    gameid = int(game_info[0]["id"])
while True:
    if cursor.execute("SELECT name FROM game WHERE id = ?", (gameid,)).fetchone() is not None:
        gameid += 1
    else:
        break

genres = (game_info[0]["genres"])
country = (pycountry.countries.get(numeric=f"{publisher_info[0]['country']}"))

insert_publisher = (publisher_info[0]['id'], publisher_info[0]['name'], country.name)
insert_game = (gameid, name, publisher_info[0]['id'], rating, release_date)

# inserting info on db
cursor.execute("INSERT INTO publisher VALUES(?, ?, ?)", insert_publisher)
cursor.execute("INSERT INTO game (`id`, `name`, `publisher_id`, `rating`, `released`) VALUES (?, ?, ?, ?, ?)", insert_game)
for genre in genres:
    cursor.execute("INSERT INTO game_genres (`game_id`, `genre_id`) VALUES (?, ?)", (gameid, genre))

con.close()

print("Game added successfully")