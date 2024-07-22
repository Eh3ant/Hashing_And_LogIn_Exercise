from flask import Flask,render_template,redirect,request,flash,session,url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User ,Feedback
from forms import UserForm,LoginForm,FeedbackForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "ehsan"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/secret')
def secret_page():
    return render_template('secret.html')

 
@app.route('/register',methods=["GET","POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username,password,email,first_name,last_name)

        db.session.add(new_user)
        db.session.commit()

        flash('Welcome! Successfully Created Your Account', 'success')
        return redirect('/secret')
    
    return render_template('/register.html',form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        
        if user:
            session.clear()
            session['user_id'] = user.username
            flash(f"Welcome back, {user.first_name}!", 'success')
            # return redirect('/secret')
            return redirect(url_for('show_user', username=user.username))
        else:
            flash("Invalid credentials.", 'danger')
            
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user(username):
    if 'user_id' not in session or session['user_id'] != username:
        flash('You must be logged in to view this page.', 'danger')
        return redirect('/login')

    user = User.query.filter_by(username=username).first_or_404()
    feedbacks = Feedback.query.filter_by(username=username).all() 
    return render_template('user.html', user=user,feedbacks=feedbacks) 



@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Successfuly Log out","info")
    return redirect('/')


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if 'user_id' not in session or session['user_id'] != username:
        flash('Access unauthorized.', 'danger')
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.filter_by(username=username).all()

    for feedback in feedbacks:
        db.session.delete(feedback)

    db.session.delete(user)
    db.session.commit()
    session.clear()
    flash('User and all feedback deleted.', 'success')
    return redirect('/')    



@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    if 'user_id' not in session or session['user_id'] != username:
        flash('Access unauthorized.', 'danger')
        return redirect('/login')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(new_feedback)
        db.session.commit()
        
        flash('Feedback added.', 'success')
        return redirect(f'/users/{username}')
    
    return render_template('add_feedback.html', form=form)



@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'user_id' not in session or session['user_id'] != feedback.username:
        flash('Access unauthorized.', 'danger')
        return redirect('/login')
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback updated.', 'success')
        return redirect(f'/users/{feedback.username}')
    
    return render_template('edit_feedback.html', form=form)



@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'user_id' not in session or session['user_id'] != feedback.username:
        flash('Access unauthorized.', 'danger')
        return redirect('/login')
    
    username = feedback.username
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted.', 'success')
    return redirect(f'/users/{username}')


