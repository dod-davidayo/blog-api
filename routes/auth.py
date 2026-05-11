from flask import Blueprint, request, jsonify
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash   #for password hashing
import re # regular expression module for passwor validation
from extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

#routes for authentication (register, login, protected route)
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
def validate_password(password):
    """Validate the password against the following criteria"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "" # if all criteria are met, return True and an empty message


# register route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error":"No input data provided"}), 400
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # check if any field is empty
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400
    
    # check if password is valid
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({"error": message}), 400

    # check if email is valid
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Invalid email address"}), 400
    
    # check if username or email already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 400

    # hash password
    hashed_password = generate_password_hash(password)

    # create new user
    new_user = User(username=username, email=email, password_hash=hashed_password, user_role='user')

    # save user to database
    db.session.add(new_user)
    db.session.commit()

    # return success message
    return jsonify({"message": "User registered successfully"}), 201

# login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() # get JSON data from request
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    email = data.get("email") # get email from data
    password = data.get("password") # get password from data

    # check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    # find user by email
    user = User.query.filter_by(email=email).first()

   


    # if user not found or password is incorrect, return error
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401
    

    
    # create access token/ jwt token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"Message": "Login successful", 
                    "access_token": access_token,
                    "user_id": user.to_dict()}), 200

# protected route
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = int(get_jwt_identity()) # get user id from token
    user = db.session.get(User, current_user_id) # get user from database
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": f"Hello, {user.username}! This is a protected route."}), 200

