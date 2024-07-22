from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20),
                         primary_key=True)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name = db.Column(db.String(30),
                          nullable=False)

    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete-orphan')
                      
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user by username and password."""
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False
    

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer,
                    primary_key=True,
                        autoincrement=True)
        
    title = db.Column(db.String(100),
                        nullable=False)
        
    content = db.Column(db.String,
                        nullable=False)
        
    username = db.Column(db.String,
                        db.ForeignKey('users.username'))

