import sqlite3

con = sqlite3.connect("games.db")
cursor = con.cursor()

cursor.executescript(
    """BEGIN;
    CREATE TABLE publisher(id INT PRIMARY KEY NOT NULL, name TEXT NOT NULL, country TEXT);
    CREATE TABLE genre(id INT PRIMARY KEY NOT NULL, name TEXT NOT NULL);
    CREATE TABLE game(id INT PRIMARY KEY NOT NULL, name TEXT NOT NULL, publisher_id INT NOT NULL,
    rating INT, released NUMERIC, FOREIGN KEY(publisher_id) REFERENCES publisher(id));
    CREATE TABLE game_genres(game_id INT NOT NULL, genre_id INT NOT NULL,
    FOREIGN KEY(game_id) REFERENCES game(id), FOREIGN KEY (genre_id) REFERENCES genre(id));
    CREATE INDEX game_names ON game(name);
    CREATE INDEX publisher_name ON publisher(name);
    CREATE VIEW my_games AS SELECT * FROM game JOIN game_genres ON game_genres.game_id = game.id JOIN publisher ON publisher.id = game.publisher_id;
    COMMIT;"""
)
cursor.close()

print(f"The database has been created successfully!")