import sqlite3
from bottle import Bottle, request, template

new = Bottle()

@new.route('/new', method='GET')
def newItem():
    if request.GET.save:
        new = request.GET.task.strip()
        connection = sqlite3.connect('App.Todo.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO TODO (TASK, STATUS) VALUES (?, ?)", (new, 1))
        newID = cursor.lastrowid
        connection.commit()
        cursor.close()
        return f'<p>The new task was inserted into the database, the ID is f{newID}</p>'
    else:
        return template('New.html')