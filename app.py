from flask import Flask
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager # for JWT authentication
from datetime import timedelta

# import db and migrate from extensions
from extensions import db, migrate


from routes.auth import auth_bp    # import auth blueprint
from routes.posts import posts_bp  # import posts blueprint



# initalize extension
app = Flask(__name__)


app.register_blueprint(auth_bp)   # register auth blueprint
app.register_blueprint(posts_bp)  # register posts blueprint




# load config
app.config.from_object(Config)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Config must come before init_app, otherwise it will not work
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 



jwt = JWTManager(app)   # initialize JWT manager comes after config

# binding
db.init_app(app)
migrate.init_app(app, db)

# for debugging
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])





if __name__ == "__main__":
    app.run(debug=True)



