from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Инициализация базы данных"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_data()

def seed_data():
    """Заполнение тестовыми данными"""
    from models import Author, Category, Book, Reader
    
    # Проверка, есть ли уже данные
    if Author.query.first():
        return
    
    # Добавление авторов
    authors = [
        Author(name="Фёдор Достоевский", country="Россия"),
        Author(name="Лев Толстой", country="Россия"),
        Author(name="Габриэль Гарсиа Маркес", country="Колумбия"),
        Author(name="Эрнест Хемингуэй", country="США"),
    ]
    for author in authors:
        db.session.add(author)
    
    # Добавление категорий
    categories = [
        Category(name="Классическая литература"),
        Category(name="Современная проза"),
        Category(name="Научная фантастика"),
        Category(name="Поэзия"),
    ]
    for category in categories:
        db.session.add(category)
    
    db.session.commit()
    
    # Добавление книг
    books = [
        Book(title="Преступление и наказание", author_id=1, category_id=1, year=1866, copies=5),
        Book(title="Война и мир", author_id=2, category_id=1, year=1869, copies=3),
        Book(title="Сто лет одиночества", author_id=3, category_id=2, year=1967, copies=4),
        Book(title="Старик и море", author_id=4, category_id=2, year=1952, copies=6),
    ]
    for book in books:
        db.session.add(book)
    
    # Добавление читателей
    readers = [
        Reader(name="Иванов Иван", email="ivanov@example.com", phone="+7-900-123-45-67"),
        Reader(name="Петрова Мария", email="petrova@example.com", phone="+7-900-234-56-78"),
        Reader(name="Сидоров Алексей", email="sidorov@example.com", phone="+7-900-345-67-89"),
    ]
    for reader in readers:
        db.session.add(reader)
    
    db.session.commit()
    print("База данных заполнена тестовыми данными!")
