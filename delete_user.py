from ext import db, app
from models import User, Product

user_id = 2

with app.app_context():
    user = Product.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
