import os
from flask import Flask
from database import init_db
from routes import main
app = Flask(__name__)
app.config['SECRET_KEY'] = 'library-secret-key-2026'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
init_db(app)
app.register_blueprint(main)

if name == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
