from ext import db, app
from models import User, Product

with app.app_context():
    new_user = User(
            name='name',
            surname='surname',
            password='password',
            username='username',
            role='guest',
            img='default.jpg'
        )
    
    db.session.add(new_user)
    db.session.commit()
