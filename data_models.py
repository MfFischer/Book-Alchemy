from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()


# Define the Author model
class Author(db.Model):
    __tablename__ = 'authors'  # Optional: Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.name})>"

    def __str__(self):
        return f"Author: {self.name}, Born: {self.birth_date}, Died: {self.date_of_death}"


# Define the Book model
class Book(db.Model):
    __tablename__ = 'books'  # Optional: Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    # Establish relationship with Author
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, isbn={self.isbn})>"

    def __str__(self):
        return f"Book: {self.title}, ISBN: {self.isbn}, Published: {self.publication_year}"
