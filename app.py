import os
from flask import Flask
from database import init_db
from routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'library-secret-key-2026'
    # Для Render используем абсолютный путь к БД, чтобы она сохранялась
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    init_db(app)
    app.register_blueprint(main)
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    # На Render debug должен быть выключен
    app.run(debug=False, host='0.0.0.0', port=port)
