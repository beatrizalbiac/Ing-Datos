# code based on https://www.geeksforgeeks.org/python/how-to-execute-a-script-in-sqlite-using-python/
import sqlite3

con = sqlite3.connect("dwh.db")

cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON;") # so the foreing keys work -> https://sqlite.org/foreignkeys.html

f = open("db/schema.sql", "r", encoding="utf-8")
sql_script = f.read()
f.close()

cur.executescript(sql_script)

cur.execute("SELECT name FROM sqlite_master WHERE type='table';") # to check it's done right. If it doesn't print anything theres smth wrong (usually in the sql file)
print(cur.fetchall())

con.commit()
con.close()


