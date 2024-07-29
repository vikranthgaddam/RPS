# run.py
from dotenv import load_dotenv
from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)