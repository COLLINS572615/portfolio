import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'portfolio.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '0353ad080a6c6a213e4255be98cca7e7e1bc90da28c65a7393b5cea5db766b19'
