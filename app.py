from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import os

# Initialize the Flask application
app = Flask(__name__)

# Use absolute path for the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data/library.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection object with the Flask app
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        return render_template('add_author.html', success=True)

    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        return render_template('add_book.html', success=True, authors=Author.query.all())

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)

if __name__ == '__main__':
    app.run(debug=True)
