from config import basedir
from app import db
from app.models import BlogPost

#create the database and db tables
db.create_all()

#insert
db.session.add(BlogPost("Very good", "I\'m very good."))
db.session.add(BlogPost("Very well", "I\'m very well."))

#commit changes
db.session.commit()