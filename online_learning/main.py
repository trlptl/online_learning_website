import os
from online_learning.models import *
from flask_jwt_extended import JWTManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from authlib.integrations.flask_client import OAuth
from online_learning.models import User, db, Course
from flask import Flask, jsonify, request, session, redirect, url_for, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from .utils import generate_random_string

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)

jwt = JWTManager(app)
admin = Admin(app)

# Check if the database file exists
database_path = os.getcwd() + "/instance/"
db_file = os.getenv('SQLALCHEMY_DATABASE_URI').replace('sqlite:///', database_path)
if not os.path.exists(db_file):
    print("IF NOT EXIST CREATE ALL")
    # Create the database and tables
    with app.app_context():
        db.init_app(app)
        db.create_all()
else:
    # Flask app is registered with 'SQLAlchemy' instance
    db.init_app(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Course, db.session))


@app.route("/")
def index():
    if session.get("user") is not None:
        user = session.get("user")
        user_email = user["email"]
        # Find the user by email
        user = User.query.filter_by(email=user_email).first()
        if user is None:
            user_password = generate_random_string(8)
            # Add user into database
            new_user = User(email=user_email, password=user_password, user_type = "Normal User")
            db.session.add(new_user)
            db.session.commit()
        courses = Course.query.all()
        return render_template("courses.html", courses=courses)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/google_authorization/")
def google_authorization():
    token = oauth.google.authorize_access_token()
    session["user"] = token["userinfo"]
    # session["google_token"] = token
    # user = oauth.google.get("userinfo")
    # Store user data in your database or session
    return redirect(url_for("index"))

@app.route('/login/')
def login():
    redirect_uri = url_for('google_authorization', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# Course master authentication
@app.route('/api/course_master_authentication/', methods=['POST'])
def course_master_authentication():
    email = request.json['email']
    password = request.json['password']

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        # Generate access token
        access_token = create_access_token(identity=user.userid)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401
    
# Api for get all courses
@app.route('/api/get_courses/', methods=['GET'])
@jwt_required()
def get_courses():
    author_id = get_jwt_identity()
    courses = Course.query.filter_by(author_id=author_id).all()
    course_list = []
    for course in courses:
        course_data = {
            'id': course.id,
            'course_name': course.course_name,
            'course_description': course.course_description,
            'course_duration': course.course_duration,
            'course_master_name': course.course_author_name,
            'price': course.price,
        }
        course_list.append(course_data)
    return {"courses": course_list}, 200


# Add Course api
@app.route('/api/add_course/', methods=['POST'])
@jwt_required()
def add_course():
    course_name = request.json['course_name']
    course_description = request.json['course_description']
    course_duration = request.json['course_duration']
    course_author_name = request.json['course_author_name']
    price = request.json['price']
    author_id = get_jwt_identity()

    # Add course into database
    new_course = Course(course_name=course_name, course_description=course_description, course_duration=course_duration,
                    course_author_name=course_author_name,price=price, author_id=author_id)

    try:
        db.session.add(new_course)
        db.session.commit()
        return jsonify(message='New course added successfully'), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(message='User already exists'), 409

# Update a course record api
@app.route('/api/update_course/<int:course_id>/', methods=['POST'])
@jwt_required()
def update_course(course_id):
    course = Course.query.get(course_id)
    if course:
        print("+"*100)
        course_name = request.json.get("course_name")
        course_description = request.json.get("course_description")
        course_duration = request.json.get("course_duration")
        course_author_name = request.json.get("course_author_name")
        price = request.json.get("price")

        course.course_name = course_name if course_name is not None else course.course_name
        course.course_description = course_description if course_description is not None else course.course_description
        course.course_duration = course_duration if course_duration is not None else course.course_duration
        course.course_author_name = course_author_name if course_author_name is not None else course.course_author_name
        course.price = price if price is not None else course.price
        db.session.commit()
        return 'Course updated successfully.'
    else:
        return 'Course not found.'