from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return 'User' + str(self.id)


@app.route('/')
def index():
    return 'Apple Lurve is a winner'

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        post_data = request.get_json()
        username = post_data.get('username').strip()
        password = post_data.get('password').strip()

        user = User.query.filter_by(username=username).first()

        if user:
            response_object = {
                'success': 'true',
                'message': 'You have successfully logged in'
            }
            return jsonify(response_object), 200

        return jsonify({
            'success': 'false',
            'error_message': 'Something went wrong, please check your credentials and try again'
        })

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        post_data = request.get_json()

        username = post_data.get('username').strip()
        email = post_data.get('email').strip()
        password = post_data.get('password').strip()

        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()
        
        response_objet = {
            'success': 'true',
            'message': 'Your account has been created successfully, please log in',
            'user': {
                'username': new_user.username,
                'email': new_user.email,
                'password': new_user.password
            }
        }
        return jsonify(response_objet), 201
    else:
        return jsonify({
            'success': 'false',
            'error_message': 'Something went wrong, please try again'
        })

@app.route('/create')
def create_article():
    return 'Create article'

@app.route('/article')
def get_article():
    return 'Get one article'

@app.route('/articles')
def get_articles():
    return 'Get all articles'

@app.route('/delete')
def delete():
    return 'Delete article'

@app.route('/update')
def update():
    return 'Update article'


if __name__ == "__main__":
    app.run(debug=True)
