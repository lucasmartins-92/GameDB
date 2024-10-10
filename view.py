import sqlite3

con = sqlite3.connect("games.db", isolation_level=None)
cursor = con.cursor()

with con:
    cursor.execute("SELECT * FROM my_games")
    print(cursor.fetchall())