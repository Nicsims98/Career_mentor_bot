from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3
import os

db = SQLAlchemy()

def init_db(app):
    """Initialize the database"""
    db.init_app(app)
    migrate = Migrate(app, db)
    app.db = db
    
    with app.app_context():
        # Drop existing database if it exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Create new tables
        db.create_all()
    
    return db
