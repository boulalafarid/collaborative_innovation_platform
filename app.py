from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Collaborative Innovation Platform!"

if __name__ == '__main__':
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)

db.create_all()  # Create the database tables
from flask import render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='To Do')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

db.create_all()  # Update the database with the new model
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_task = Task(title=title, description=description, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks'))
    all_tasks = Task.query.all()
    return render_template('tasks.html', tasks=all_tasks)
from flask_uploads import UploadSet, configure_uploads, ALL

documents = UploadSet('documents', ALL)
app.config['UPLOADED_DOCUMENTS_DEST'] = 'uploads/documents'
configure_uploads(app, documents)
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    version = db.Column(db.Integer, default=1)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_path = db.Column(db.String(150), nullable=False)

db.create_all()  # Update the database with the new model
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        if file:
            filename = documents.save(file)
            new_document = Document(title=title, uploaded_by=current_user.id, file_path=filename)
            db.session.add(new_document)
            db.session.commit()
            return redirect(url_for('upload'))
    return render_template('upload.html')
from flask_uploads import UploadSet, configure_uploads, ALL

documents = UploadSet('documents', ALL)
app.config['UPLOADED_DOCUMENTS_DEST'] = 'uploads/documents'
configure_uploads(app, documents)
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    version = db.Column(db.Integer, default=1)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_path = db.Column(db.String(150), nullable=False)

db.create_all()  # Update the database with the new model
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        if file:
            filename = documents.save(file)
            new_document = Document(title=title, uploaded_by=current_user.id, file_path=filename)
            db.session.add(new_document)
            db.session.commit()
            return redirect(url_for('upload'))
    return render_template('upload.html')
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

    @app.route('/chat')
    @login_required
    def chat():
        return render_template('chat.html')
if __name__ == '__main__':
    socketio.run(app, debug=True)
