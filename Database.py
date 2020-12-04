import sqlite3

"""
This generates a database-file App.Todo.db with tables called todo and three columns id, task, and status. 
id is a unique id for each row, which is used later on to reference the rows. The column task holds the 
text which describes the task, it can be max 100 characters long. Finally, the column status is used to
 mark a task as open (value 1) or closed (value 0).
"""

connection = sqlite3.connect('App.Todo.db')
connection.execute("CREATE TABLE TODO (ID INTEGER PRIMARY KEY, TASK char(100) NOT NULL, STATUS bool NOT NULL)")
connection.execute("INSERT INTO TODO (TASK,STATUS) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
connection.execute("INSERT INTO TODO (TASK,STATUS) VALUES ('Visit the Python website',1)")
connection.execute("INSERT INTO TODO (TASK,STATUS) VALUES ('Test various editors for and check the syntax highlighting',1)")
connection.execute("INSERT INTO TODO (TASK,STATUS) VALUES ('Choose your favorite WSGI-Framework',0)")
connection.commit()