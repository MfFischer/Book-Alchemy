import unittest
from datetime import date
from app import app, db, Author, Book


class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a blank database before each test."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Push an application context
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()  # Renamed to `client` to avoid conflict

        # Create all the tables
        db.create_all()

        # Add a sample author and book to the test database
        self.author = Author(name="J.K. Rowling", birth_date=date(1965, 7, 31))
        db.session.add(self.author)
        db.session.commit()

        self.book = Book(isbn="1234567890123", title="Test Book", publication_year=2020, author_id=self.author.id,
                         rating=8)
        db.session.add(self.book)
        db.session.commit()

    def tearDown(self):
        """Destroy the database after each test."""
        db.session.remove()
        db.drop_all()

        # Pop the application context
        self.app_context.pop()

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)

    def test_add_author(self):
        """Test adding a new author."""
        response = self.client.post('/add_author', data=dict(
            name="New Author",
            birth_date="1980-01-01",
            date_of_death=""
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Author', response.data)

    def test_add_book(self):
        """Test adding a new book."""
        response = self.client.post('/add_book', data=dict(
            isbn="9876543210987",
            title="New Book",
            publication_year=2021,
            author_id=self.author.id,
            rating=7
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Book', response.data)

    def test_search(self):
        """Test searching for a book."""
        response = self.client.get('/search?keyword=Test', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)

    def test_book_detail(self):
        """Test that book detail page loads correctly."""
        response = self.client.get(f'/book/{self.book.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)

    def test_delete_book(self):
        """Test deleting a book."""
        response = self.client.post(f'/book/{self.book.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Book', response.data)

    def test_author_detail(self):
        """Test that author detail page loads correctly."""
        response = self.client.get(f'/author/{self.author.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'J.K. Rowling', response.data)


if __name__ == '__main__':
    unittest.main()
