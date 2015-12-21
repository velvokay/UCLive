from config import basedir
from app import db
from app.models import BlogPost

#create the database and db tables
db.create_all()

#insert
db.session.add(BlogPost("One", "Connection established."))
db.session.add(BlogPost("Two", "Hello internet!"))

#commit changes
db.session.commit()