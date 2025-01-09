from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer) 
       
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    img = db.Column(db.String)
    
    def __init__(self, username, password, name=None, surname=None, role="Guest", img=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.surname = surname
        self.role = role
        self.img = img
        
    def check_password(self, password):
        return check_password_hash(self.password, password)


    
@login_manager.user_loader    
def load_user(user_id):
   return User.query.get(user_id)