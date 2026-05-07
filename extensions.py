# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# import migration tool
from flask_migrate import Migrate

# create db instance
db = SQLAlchemy()

# create migrate instance
migrate = Migrate()