from flask import Flask, render_template, redirect, session, flash, url_for
from models import db, User, Feedback
from forms import RegistrationForm, LoginForm, FeedbackForm
from flask_login import login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://equansa00:1Chriss1@localhost/flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['username'] = user.username
            return redirect('/secret')
        flash('Invalid login credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/secret')
def secret():
    if 'username' not in session:
        flash("Please login to access this page.", "danger")
        return redirect('/login')
    return "You made it!"


@app.route('/users/<username>')
def user_profile(username):
    if 'username' not in session or session['username'] != username:
        return redirect('/login')
    user = User.query.get(username)
    return render_template('user.html', user=user)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        return redirect('/login')
    # Implement form logic and render template

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        return redirect('/login')
    db.session.delete(feedback)
    db.session.commit()
    return redirect(f'/users/{feedback.username}')

@app.route('/users/<username>')
@login_required
def user_detail(username):
    if current_user.username != username:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.filter_by(username=username).all()
    return render_template('user_detail.html', user=user, feedbacks=feedbacks)

@app.route('/users/<username>/delete', methods=["POST"])
@login_required
def delete_user(username):
    if current_user.username != username:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    # Delete feedbacks, then user
    Feedback.query.filter_by(username=username).delete()
    User.query.filter_by(username=username).delete()
    session.clear()
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
@login_required
def add_feedback(username):
    if current_user.username != username:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = FeedbackForm()
    # Process form & save data...
    return render_template('feedback_form.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose another one.', 'danger')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password, email=form.email.data,
                    first_name=form.first_name.data, last_name=form.last_name.data)
        try:
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            return redirect('/secret')
        except IntegrityError:  # Ensure you've imported IntegrityError at the top
            db.session.rollback()
            flash('An error occurred. Perhaps the username or email already exists.', 'danger')

    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
