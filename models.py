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

    username = db.Column(db.String(20),
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

    db.relationship("Note", backref="users")
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name) :
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        return cls(
            username=username, 
            password=hashed, 
            email=email, 
            first_name=first_name, 
            last_name=last_name
            )

            # Have the class = to a variable (user)
            # use db.session.add(user) alot cleaner and less redundent
        
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        # User.one_none is fine with an id, but here it's better with .get()
        user = cls.query.get(username)

        if user and bcrypt.check_password_hash(user.password, pwd):
            # return user instance
            return user
        else:
            return False

class Note(db.Model):
    """User Model"""

    __tablename__ = "notes"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)

    title = db.Column(db.String(100), 
                    nullable=False)

    content = db.Column(db.Text, 
                    nullable=False)

    owner = db.Column(db.String(20),
                    db.ForeignKey("users.username"), 
                    nullable=False)


    