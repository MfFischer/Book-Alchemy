from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object for database operations
db = SQLAlchemy()


class Author(db.Model):
    """
    Model representing an author in the library system.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # Establish a relationship with the Book model,
    # enabling cascading deletes for associated books
    books = db.relationship('Book', backref='author', cascade="all, delete-orphan")

    def __repr__(self):
        """Provide a string representation of the Author object."""
        return f'<Author {self.name}>'


class Book(db.Model):
    """
    Model representing a book in the library system.
    """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    # Foreign key linking the book to its author; cascades on delete
    author_id = db.Column(db.Integer,
                          db.ForeignKey('authors.id', ondelete="CASCADE"), nullable=False)

    # Rating column allows users to rate the book; values should be between 1 and 10
    rating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide a string representation of the Book object."""
        return f'<Book {self.title}>'
