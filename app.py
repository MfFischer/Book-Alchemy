from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
import os
from datetime import datetime

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
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        # Convert strings to date objects
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

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


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')

    if keyword:
        search_pattern = f"%{keyword.lower()}%"
        print(f"Search pattern: {search_pattern}")  # Debug: Check the search pattern
        results = Book.query.filter(db.func.lower(Book.title).like(search_pattern)).all()
        print(f"Results: {results}")  # Debug: Check the results

        if results:
            return render_template('search_results.html', books=results, keyword=keyword)
        else:
            return render_template('search_results.html', books=[], keyword=keyword, no_results=True)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
