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

@route('/edit/static/css/<filename>')
def serverStaticEditCSS(filename):
    return serverStaticCSS(filename)

@route('/edit/static/js/<filename>')
def serverStaticEditJS(filename):
    return serverStaticJS(filename)

@route('/static/css/<filename>')
def serverStaticCSS(filename):
    """
    Why is important added the Cache-Control header?

    The right caching strategy can help improve site performance through:

    - Shorter load times
    - Reduced bandwidth
    - Reduced server costs
    - Having predictable behavior across browsers

    Currently about ~50% of resources on the web can’t be cached due to their configuration
    Reference: https://webhint.io/docs/user-guide/hints/hint-http-cache/

    Reference: https://stackoverflow.com/a/24748094
    :param filename: Static filename, generally css files
    :return: The static file, generally css files
    """
    response = static_file(filename, root='./static/css/')
    # For those wondering, 604800 is the number of seconds in a week. 604800 / 60 / 60 / 24 = 7
    response.set_header("Cache-Control", "public, max-age=604800")
    return response

@route('/static/js/<filename>')
def serverStaticJS(filename):
    return static_file(filename, root='./static/js/')

@route('/static/img/png/<filename>')
def serverStaticPNG(filename):
    return static_file(filename, root='./static/img/png')

@route('/static/img/svg/<filename>')
def serverStaticSVG(filename):
    return static_file(filename, root='./static/img/svg')

run(host='localhost', port=8080, debug=True, reloader=True)