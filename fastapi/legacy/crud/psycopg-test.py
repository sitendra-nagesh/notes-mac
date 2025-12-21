import psycopg2
conn = psycopg2.connect(database = "fastapi", user = "postgres", host="localhost")
curr = conn.cursor()

# READ
query = curr.execute("SELECT * FROM posts;")
returnVal = curr.fetchall()

# INSERT

# query = curr.execute("INSERT into posts (title, content) VALUES (%s, %s);", ("6th post", "content of 6th post",))
# conn.commit()

query = curr.execute("SELECT * FROM posts;")
returnVal = curr.fetchall()


print(returnVal)

curr.close()
conn.close()