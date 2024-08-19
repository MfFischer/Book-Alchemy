from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object for database interactions
db = SQLAlchemy()


# Define the Author model, representing the 'authors' table
class Author(db.Model):
    __tablename__ = 'authors'  # Set the table name

    # Define the columns of the 'authors' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key with auto-increment
    name = db.Column(db.String(150), nullable=False)  # Name of the author (non-nullable)
    birth_date = db.Column(db.Date, nullable=True)  # Optional birth date of the author
    date_of_death = db.Column(db.Date, nullable=True)  # Optional date of death of the author

    def __repr__(self):
        """Provide a string representation for debugging."""
        return f"<Author(id={self.id}, name={self.name})>"

    def __str__(self):
        """Provide a readable string representation of the Author."""
        return f"Author: {self.name}, Born: {self.birth_date}, Died: {self.date_of_death}"


# Define the Book model, representing the 'books' table
class Book(db.Model):
    __tablename__ = 'books'  # Set the table name

    # Define the columns of the 'books' table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key with auto-increment
    isbn = db.Column(db.String(13), unique=True, nullable=False)  # ISBN of the book (unique and non-nullable)
    title = db.Column(db.String(200), nullable=False)  # Title of the book (non-nullable)
    publication_year = db.Column(db.Integer, nullable=False)  # Publication year of the book (non-nullable)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)  # Foreign key to 'authors' table

    # Establish a relationship with the Author model
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        """Provide a string representation for debugging."""
        return f"<Book(id={self.id}, title={self.title}, isbn={self.isbn})>"

    def __str__(self):
        """Provide a readable string representation of the Book."""
        return f"Book: {self.title}, ISBN: {self.isbn}, Published: {self.publication_year}"
