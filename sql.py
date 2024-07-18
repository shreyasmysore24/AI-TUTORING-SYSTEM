import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('test_scores.db')
cursor = conn.cursor()

# Create table (if it doesn't exist)
cursor.execute('''
CREATE TABLE IF NOT EXISTS test_scores (
    test_no INTEGER PRIMARY KEY AUTOINCREMENT,
    date_and_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    maths INTEGER,
    science INTEGER,
    social INTEGER,
    category TEXT
)
 ''')
# cursor.execute('DELETE FROM test_scores')


# data_to_insert = [
#     (3, 3, 3, 'hard'),
#     (3, 2, 3, 'hard'),
#     (2, 1, 2, 'medium')
# ]


# for data in data_to_insert:
#     cursor.execute('''
#     INSERT INTO test_scores (maths, science, social, category)
#     VALUES (?, ?, ?, ?)
#     ''', data)

sc=cursor.execute("""SELECT maths, science, social, category
FROM test_scores
ORDER BY test_no DESC
;""")
# sc=cursor.execute("""SELECT AVG(maths) AS average_maths
# FROM test_scores
# ORDER BY test_no DESC
# LIMIT 3;
# """)

for s in sc:
 print(s)



# result = cursor.fetchall()
# print(str(list(result[0])[0]))


conn.commit()
conn.close()


