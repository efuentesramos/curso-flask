from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from my_app.config import DevConfig

app = Flask(__name__)


app.config.from_object(DevConfig)

db=SQLAlchemy(app)
migrate = Migrate(app,db)

#login
login_manager = LoginManager()
login_manager.init_app(app)

from my_app.tasks.controller import taskRoute
from my_app.auth.controllers import authRoute

app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)

# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():
    name = request.args.get('name','Desarrollo')
    return render_template('index.html', otra=name)