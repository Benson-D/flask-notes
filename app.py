from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from forms import RegistrationForm, LoginForm
from models import connect_db, db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()


@app.get('/')
def redirect_register():
    """Redirects to the register"""

    return redirect('/register')

@app.route("/register", methods=["GET", "POST"])
def display_register():
    """Displays register form html"""

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # breakpoint()
        User.register(username, password, email, first_name, last_name)

        session["username"] = username # keep logged in

        db.session.commit()

        return redirect('/secret')

    else: 
        return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Displays register form html"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["username"] = username # keep logged in
            return redirect('/secret')
        else:
            form.username.errors = ["Incorrect username or password."]
    return render_template("login_form.html", form=form)
    
@app.get("/secret")
def secret_page():
    return render_template("secret.html")