from database_model import db, User
#clears out database of all models
db.drop_all();
#Creates new database according to the model declared in 'database_model.py'
db.create_all()

#Creates new classes based off models in 'database_model.py'
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')

#Adds classes to database
db.session.add(admin)
db.session.add(guest)
db.session.commit()

#Queries database
print(User.query.all())