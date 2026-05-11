from flask import Blueprint, request, jsonify
from models.post import Post
from extensions import db
from flask_jwt_extended import  create_access_token, jwt_required, get_jwt_identity

# routes for posts (create, read, update, delete)
posts_bp = Blueprint("posts", __name__, url_prefix="/posts")



# create post route
@posts_bp.route("/", methods=["POST"])
@jwt_required() # only login users can create posts
def create_post():

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    
    # get current user id from JWT token
    current_user_id = int(get_jwt_identity())
    
    
    # create new post
    new_post = Post(title=title, content=content, user_id=current_user_id)

    # save post to database
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", 
                    "post": new_post.to_dict()}), 201


# read post
@posts_bp.route("/", methods=["GET"])
def get_posts():

    posts = Post.query.all()

    return jsonify([post.to_dict() for post in posts]), 200

#read single post
@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = db.session.get(Post, post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    return jsonify(post.to_dict()), 200

# update posts
@posts_bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    post = db.session.get(Post, post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    # check if the current user is the owner of the post
    current_user_id = int(get_jwt_identity())
    if post.user_id != current_user_id:
        return jsonify({"error": "Unauthorized to update this post"}), 403

    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if title:
        post.title = title
    if content:
        post.content = content

    db.session.commit()

    return jsonify({"message": "Post updated successfully", 
                    "post": post.to_dict()}), 200



#delete posts
@posts_bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    post = db.session.get(Post, post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    # check if the current user is the owner of the post
    current_user_id = int(get_jwt_identity())
    if post.user_id != current_user_id:
        return jsonify({"error": "Unauthorized to delete this post"}), 403

    # delete the post
    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200

# admin deleting a post
@posts_bp.route("/admin/<int:post_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_post(post_id):
    post = db.session.get(Post, post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404

    # check if the current user is an admin
    current_user_id = int(get_jwt_identity())
    from models.users import User
    user = db.session.get(User, current_user_id)
    if user.user_role != 'admin':
        return jsonify({"error": "Unauthorized to delete this post"}), 403

    # delete the post
    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully by admin"}), 200

# refresh token route
@posts_bp.route("/refresh", methods=["POST"])
def refresh_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200
