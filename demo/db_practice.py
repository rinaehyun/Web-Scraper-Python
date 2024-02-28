import sqlite3

# Establish a connection and a cursor
connection = sqlite3.connect("../databases/match-data.db")
cursor = connection.cursor()

# Query certain columns
cursor.execute("SELECT * FROM MatchInfos")
rows = cursor.fetchall()
print(rows)

# Insert new rows
new_rows = [('Sport-Club Freiburg', 'FC Bayern München'),
            ('SV Darmstadt 98', 'FC Augsburg'),
            ('1. FC Heidenheim 1846', 'Eintracht Frankfurt'),
            ('VfL Bochum 1848', 'RB Leipzig'),
            ('1. FSV Mainz 05', 'Borussia Mönchengladbach'),
            ('1. FC Union Berlin', 'Borussia Dortmund'),
            ('VfL Wolfsburg', 'VfB Stuttgart'),
            ('1. FC Köln', 'Bayer 04 Leverkusen'),
            ('TSG Hoffenheim', 'SV Werder Bremen')]

cursor.executemany("INSERT INTO MatchInfos VALUES('24. Spieltag', ?, ?)", new_rows)
connection.commit()

# Query certain columns
cursor.execute("SELECT * FROM MatchInfos")
rows = cursor.fetchall()
print(rows)