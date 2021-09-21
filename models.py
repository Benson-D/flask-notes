from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt 

bcrypt = Bcrypt()

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    user_name = db.Column(db.String(20),
                   primary_key=True,
                   nullable=False)

    password = db.Column(db.String(100), 
                    nullable=False)

    email = db.Column(db.String(50), 
                    unique=True, 
                    nullable=False)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)
    
    @classmethod
    def register(username, pwd, email, first_name, last_name) :
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # return instance of user w/username and hashed pwd
        user = User(
            username=username, 
            password=hashed, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
            )

        db.session.add(user)   
        return user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return False

