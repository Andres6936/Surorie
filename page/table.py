import sqlite3
from bottle import Bottle, template

app = Bottle()

@app.route('/')
def __app():
    connection = sqlite3.connect('App.Todo.db')
    cursor = connection.cursor()
    cursor.execute('SELECT ID, TASK FROM TODO WHERE STATUS LIKE "1"')
    result = cursor.fetchall()
    cursor.close()
    return template('Table.html', rows=result)