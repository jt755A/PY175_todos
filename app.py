from uuid import uuid4

from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from todos.utils import error_for_list_title, find_list_by_id, error_for_todo_title, find_todo_by_id
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    return render_template('new_list.html')

@app.route("/lists")
def get_lists():
    return render_template('lists.html', lists=session['lists'])

@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()

    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)

    session['lists'].append({
        'id': str(uuid4()),
        'title': title,
        'todos': [],
        })

    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

    flash("The title must be between 1 and 100 characters.", "error")
    return render_template('new_list.html', title=title)

@app.route("/lists/<list_id>")
def get_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    return render_template('list.html', lst=lst)

@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form['todo'].strip()
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")

    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template('list.html', lst=lst)

    lst['todos'].append({
        'id': str(uuid4()),
        'title': todo_title,
        'completed': False,
    })

    flash("The todo has been created", "success")
    session.modified = True
    # return render_template('list.html', lst=lst)
    return redirect(url_for('get_list', list_id=list_id))

@app.route("/lists/<list_id>/todos/<todo_id>/toggle", methods=["POST"])
def toggle_todo(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    todo = find_todo_by_id(todo_id, lst)
    if not lst:
        raise NotFound(description="List not found")
    elif not todo:
        raise NotFound(description="Todo not found")

    new_completion_status = request.form['completed']
    todo['completed'] = new_completion_status
    flash("Todo status was updated", "success")
    session.modified = True

    return redirect(url_for('get_list', list_id=list_id))


if __name__ == "__main__":
    app.run(debug=True, port=5003)