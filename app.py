from flask import Flask
from config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# initalize extension
app = Flask(__name__)

db = SQLAlchemy()
migrate = Migrate(app, db) # alembic migration tool

# load config
# app.config.from_object(Config)

# Config must come before init_app, otherwise it will not work
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   


# binding
db.init_app(app)
migrate.init_app(app, db)

# for debugging
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])





if __name__ == "__main__":
    app.run(debug=True)



