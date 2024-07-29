from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ratings = db.relationship('Rating', backref='class', lazy=True)
    comments = db.relationship('Comment', backref='class', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        login_user(user)
        return jsonify({'message': 'Logged in'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/classes', methods=['GET'])
def get_classes():
    classes = Class.query.all()
    return jsonify([{'id': cls.id, 'name': cls.name} for cls in classes])

@app.route('/rate', methods=['POST'])
@login_required
def rate_class():
    data = request.json
    rating = Rating(stars=data['stars'], user_id=current_user.id, class_id=data['class_id'])
    db.session.add(rating)
    db.session.commit()
    return jsonify({'message': 'Rating submitted'})

@app.route('/comments', methods=['GET', 'POST'])
def handle_comments():
    if request.method == 'GET':
        class_id = request.args.get('class_id')
        comments = Comment.query.filter_by(class_id=class_id).all()
        return jsonify([{'content': comment.content, 'user': comment.user.username} for comment in comments])
    elif request.method == 'POST':
        if current_user.is_authenticated:
            data = request.json
            comment = Comment(content=data['content'], user_id=current_user.id, class_id=data['class_id'])
            db.session.add(comment)
            db.session.commit()
            return jsonify({'message': 'Comment submitted'})
        return jsonify({'message': 'Login required'}), 401

@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
