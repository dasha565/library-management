from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from models import Book, Reader, Loan, Author, Category
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Главная страница со статистикой"""
    total_books = Book.query.count()
    total_readers = Reader.query.count()
    active_loans = Loan.query.filter_by(is_returned=False).count()
    
    # SQL-запрос для статистики по категориям
    categories_stats = db.session.query(
        Category.name,
        db.func.count(Book.id)
    ).join(Book).group_by(Category.name).all()
    
    return render_template('index.html',
                         total_books=total_books,
                         total_readers=total_readers,
                         active_loans=active_loans,
                         categories_stats=categories_stats)

@main.route('/books')
def books():
    """Список всех книг"""
    books = Book.query.join(Author).join(Category).all()
    return render_template('books.html', books=books)

@main.route('/books/add', methods=['GET', 'POST'])
def add_book():
    """Добавление новой книги"""
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        category_id = request.form['category_id']
        year = request.form['year']
        copies = request.form['copies']
        
        new_book = Book(
            title=title,
            author_id=author_id,
            category_id=category_id,
            year=int(year),
            copies=int(copies)
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('main.books'))
    
    authors = Author.query.all()
    categories = Category.query.all()
    return render_template('add_book.html', authors=authors, categories=categories)

@main.route('/readers')
def readers():
    """Список читателей"""
    readers = Reader.query.all()
    return render_template('readers.html', readers=readers)

@main.route('/readers/add', methods=['GET', 'POST'])
def add_reader():
    """Добавление нового читателя"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        new_reader = Reader(name=name, email=email, phone=phone)
        db.session.add(new_reader)
        db.session.commit()
        flash('Читатель успешно добавлен!', 'success')
        return redirect(url_for('main.readers'))
    
    return render_template('add_reader.html')

@main.route('/loans')
def loans():
    """Список выдач"""
    loans = Loan.query.join(Book).join(Reader).all()
    return render_template('loans.html', loans=loans)

@main.route('/loans/add', methods=['GET', 'POST'])
def add_loan():
    """Выдача книги"""
    if request.method == 'POST':
        book_id = request.form['book_id']
        reader_id = request.form['reader_id']
        
        new_loan = Loan(book_id=book_id, reader_id=reader_id)
        db.session.add(new_loan)
        db.session.commit()
        flash('Книга успешно выдана!', 'success')
        return redirect(url_for('main.loans'))
    
    books = Book.query.all()
    readers = Reader.query.all()
    return render_template('add_loan.html', books=books, readers=readers)

@main.route('/loans/<int:loan_id>/return', methods=['POST'])
def return_loan(loan_id):
    """Возврат книги"""
    loan = Loan.query.get_or_404(loan_id)
    loan.is_returned = True
    loan.return_date = datetime.utcnow()
    db.session.commit()
    flash('Книга возвращена!', 'success')
    return redirect(url_for('main.loans'))
