import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate

from data_models import db, Author, Book

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database using an absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data/library.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the database instance to the app
db.init_app(app)

# Initialize Flask-Migrate with the app and database instance
migrate = Migrate(app, db)


@app.route('/')
def home():
    """Route to display the home page with a list of all books."""
    books = Book.query.all()

    # Debugging: Output the number of books found
    print(f"Books found: {len(books)}")
    for book in books:
        # Debugging: Output each book and its author
        print(f"Book: {book.title} by {book.author.name}")

    return render_template('home.html', books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Route to add a new author to the database."""
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        # Convert strings to date objects, if provided
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        # Create a new Author object
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        # Add the new author to the session and commit to the database
        db.session.add(new_author)
        db.session.commit()

        # Render the template with a success message
        return render_template('add_author.html', success=True)

    # Render the form for adding a new author
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Route to add a new book to the database."""
    if request.method == 'POST':
        # Get the form data
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        rating = request.form.get('rating')  # Get the rating from the form

        # Create a new Book object with the rating
        new_book = Book(isbn=isbn, title=title, publication_year=publication_year,
                        author_id=author_id, rating=rating)

        # Add the new book to the session and commit to the database
        db.session.add(new_book)
        db.session.commit()

        # Render the template with a success message and the list of authors
        return render_template('add_book.html', success=True, authors=Author.query.all())

    # Render the form for adding a new book with a list of authors
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/search', methods=['GET'])
def search():
    """Route to search for books by title."""
    keyword = request.args.get('keyword', '')

    if keyword:
        # Create a search pattern for case-insensitive matching
        search_pattern = f"%{keyword.lower()}%"

        # Debugging: Output the search pattern
        print(f"Search pattern: {search_pattern}")

        # Query the database for books matching the search pattern
        results = Book.query.filter(db.func.lower(Book.title).like(search_pattern)).all()

        # Debugging: Output the search results
        print(f"Results: {results}")

        # Render the search results page
        return render_template('search_results.html', books=results, keyword=keyword)

    # Redirect to the homepage if no keyword is provided
    return redirect(url_for('home'))


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Route to delete a book and possibly its author if no other books exist."""
    # Fetch the book by its ID
    book = Book.query.get_or_404(book_id)

    # Store the author ID before deleting the book
    author_id = book.author_id

    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()

    # Check if the author has any other books
    author_books = Book.query.filter_by(author_id=author_id).all()

    # If the author has no other books, delete the author
    if not author_books:
        author = Author.query.get(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()

    # Redirect to the homepage with a success message
    return redirect(url_for('home', message="Book deleted successfully!"))


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """Route to display details for a specific book."""
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/author/<int:author_id>')
def author_detail(author_id):
    """Route to display details for a specific author."""
    author = Author.query.get_or_404(author_id)
    return render_template('author_detail.html', author=author)


@app.route('/manage_deletions', methods=['GET', 'POST'])
def manage_deletions():
    """
    Route for managing deletions and updates of authors and books.
    Handles POST requests for deleting authors, deleting books,
    updating author information, and updating book ratings.
    """
    authors = Author.query.all()
    books = Book.query.all()

    if request.method == 'POST':
        # Handle deletion of an author and all associated books
        if 'delete_author' in request.form:
            author_id = request.form.get('author_id')
            author = Author.query.get_or_404(author_id)
            db.session.delete(author)
            db.session.commit()
            return redirect(
                url_for('manage_deletions',
                        message=f"Author '{author.name}' and all associated books have been deleted.")
            )

        # Handle deletion of a specific book
        elif 'delete_book' in request.form:
            book_id = request.form.get('book_id')
            book = Book.query.get_or_404(book_id)
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('manage_deletions',
                                    message=f"Book '{book.title}' has been deleted."))

        # Handle update of an author's details
        elif 'update_author' in request.form:
            author_id = request.form.get('author_id')
            author = Author.query.get_or_404(author_id)
            author.name = request.form.get('name')
            author.birth_date = request.form.get('birth_date')
            author.date_of_death = request.form.get('date_of_death')
            db.session.commit()
            return redirect(url_for('manage_deletions',
                                    message=f"Author '{author.name}' has been updated."))

        # Handle update of a book's rating
        elif 'update_book' in request.form:
            book_id = request.form.get('book_id')
            book = Book.query.get_or_404(book_id)
            book.title = request.form.get('title')
            book.publication_year = request.form.get('publication_year')
            book.rating = request.form.get('rating')
            db.session.commit()
            return redirect(url_for('manage_deletions',
                                    message=f"Book '{book.title}' has been updated with new details."))

    # Render the management page with the list of authors and books
    return render_template('manage_deletions.html', authors=authors, books=books)


@app.route('/book/<int:book_id>/rate', methods=['POST'])
def rate_book(book_id):
    """Route to handle rating submission for a book."""
    book = Book.query.get_or_404(book_id)
    rating = request.form.get('rating')

    # Update the book's rating
    book.rating = int(rating)
    db.session.commit()

    return redirect(url_for('book_detail', book_id=book_id))


if __name__ == '__main__':
    app.run(debug=True)
