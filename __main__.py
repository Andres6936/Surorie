import sqlite3
from page.table import app
from page.new import new

from bottle import Bottle, template, request, static_file

main = Bottle()

@main.route('/edit/<number>', method='GET')
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
        cursor.close()
        return template('Edit.html', modeEdit=False, number=number)
    else:
        connection = sqlite3.connect('App.Todo.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT TASK FROM TODO WHERE ID LIKE {number}')
        currentItem = cursor.fetchone()
        cursor.close()
        return template('Edit.html', modeEdit=True, old=currentItem, number=number)

@main.route('/edit/static/css/<filename>')
def serverStaticEditCSS(filename):
    return serverStaticCSS(filename)

@main.route('/edit/static/js/<filename>')
def serverStaticEditJS(filename):
    return serverStaticJS(filename)

@main.route('/static/css/<filename>')
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

@main.route('/static/js/<filename>')
def serverStaticJS(filename):
    return static_file(filename, root='./static/js/')

@main.route('/static/img/png/<filename>')
def serverStaticPNG(filename):
    return static_file(filename, root='./static/img/png')

@main.route('/static/img/svg/<filename>')
def serverStaticSVG(filename):
    return static_file(filename, root='./static/img/svg')

if __name__ == '__main__':
    main.merge(app)
    main.merge(new)
    main.run(host='localhost', port=8080, debug=True, reloader=True)