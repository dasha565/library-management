from database import db
from datetime import datetime

class Author(db.Model):
    """Таблица авторов"""
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    country = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с книгами
    books = db.relationship('Book', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<Author {self.name}>'

class Category(db.Model):
    """Таблица категорий"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Связь с книгами
    books = db.relationship('Book', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Book(db.Model):
    """Таблица книг"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    year = db.Column(db.Integer)
    copies = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с выдачами
    loans = db.relationship('Loan', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Reader(db.Model):
    """Таблица читателей"""
    __tablename__ = 'readers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с выдачами
    loans = db.relationship('Loan', backref='reader', lazy=True)
    
    def __repr__(self):
        return f'<Reader {self.name}>'

class Loan(db.Model):
    """Таблица выдач книг"""
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Loan {self.id}>'
