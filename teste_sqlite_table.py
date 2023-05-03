import sqlite3

# connect to the database
conn = sqlite3.connect('mydatabase.db')

# create a cursor object
cursor = conn.cursor()

# create the table with an auto-generated position column
cursor.execute('''CREATE TABLE IF NOT EXISTS championship_table
                (position INTEGER PRIMARY KEY,
                 team_name TEXT,
                 points INTEGER,
                 goals_difference INTEGER)''')

# # insert some sample data
# data = [('Manchester United', 20, 10),
#         ('Chelsea', 18, 8),
#         ('Liverpool', 18, 6),
#         ('Arsenal', 15, 3),
#         ('Tottenham', 14, 1)]

# for row in data:
#     cursor.execute("INSERT INTO championship_table (team_name, points, goals_difference) VALUES (?, ?, ?)", row)

# select the data from the table with an ordered position column
cursor.execute("SELECT row_number() OVER (ORDER BY points DESC, goals_difference DESC) AS position, team_name, points, goals_difference FROM championship_table")

# print the results
rows = cursor.fetchall()
for row in rows:
    print(row)

# commit the changes and close the connection
conn.commit()
conn.close()