from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # Just references this file
# Three forward slashes below is a relative path, four is an absolute path
# This tells our app where our db is located
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)  # Initialising database

# A Model is a Python class which represents the database table and its attributes
# map to the column of the table. A model class inherits from db.Model and defines columns as an instance of db.Column class


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # The __repr__ will return a string every time we create a new element
    def __repr__(self):
        # Every time we create new element it will return Task plus the id of that task
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Above: method='POST' is written in the form section in index.html; we are accessing that section here
        # Below: form written to access the form we created in index.html, and 'content' for the id of the input we want to get the contents of
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # Now try and push the input / content to the database
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')  # Returns redirect back to our homepage
        except:
            return 'There was an issue adding your task'

    else:
        # Orders current tasks by date_created column from newest to oldest
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# Deletes task by deleting primary key which is the id
# The string passed to app.route just determines what will be added to the url when this action is carried out
@app.route('/delete/<int:id>')
def delete(id):
    # Attempts to get task by id and if it doesn't it will just 404
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting your task'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    # debug=True will cause any errors we might have to display on the webpage
    app.run(debug=True)
