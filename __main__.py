import sqlite3
from bottle import route, run, template, request, static_file

@route('/app')
def app():
    connection = sqlite3.connect('App.Todo.db')
    cursor = connection.cursor()
    cursor.execute('SELECT ID, TASK FROM TODO WHERE STATUS LIKE "1"')
    result = cursor.fetchall()
    cursor.close()
    return template('Table.html', rows=result)

@route('/new', method='GET')
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

@route('/edit/<number:int>', method='GET')
def edit(number):
    if request.GET.save:
        editTask = request.GET.task.strip()
        status = request.GET.status.strip()
        if status == 'open':
            status = 1
        else:
            status = 0
        connection = sqlite3.connect('App.Todo.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE TODO SET TASK=?, STATUS=? WHERE ID LIKE ?', (editTask, status, number))
        connection.commit()
        return f'<p>The item number {number} was successfully updated</p>'
    else:
        connection = sqlite3.connect('App.Todo.db')
        cursor = connection.cursor()
        cursor.execute('SELECT TASK FROM TODO WHERE ID LIKE ?', (str(number)))
        currentItem = cursor.fetchone()
        return template('Edit.html', old=currentItem, number=number)

@route('/static/css/<filename>')
def serverStatic(filename):
    return static_file(filename, root='./static/css/')

run(host='localhost', port=8080, debug=True, reloader=True)