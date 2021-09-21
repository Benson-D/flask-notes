from flask import Flask, redirect, render_template, session, flash
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
        user = User.register(username, password, email, first_name, last_name)

        session["username"] = user.username # keep logged in

        db.session.add(user)
        db.session.commit()

        return redirect(f'users/{username}')

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
            session["username"] = user.username # keep logged in
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ["Incorrect username or password."]
    return render_template("login_form.html", form=form)
    
@app.get("/users/<username>")
def secret_page(username):

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:

        user = User.query.get(username)
        return render_template('user.html', user=user)

@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    # Remove "user_id" if present, but no errors if it wasn't
    session.pop("username", None)

    return redirect("/")