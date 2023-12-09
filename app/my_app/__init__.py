from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from my_app.config import DevConfig

app = Flask(__name__)


app.config.from_object(DevConfig)

db=SQLAlchemy(app)
migrate = Migrate(app,db)

from my_app.tasks.controller import taskRoute

app.register_blueprint(taskRoute)

# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():
    name = request.args.get('name','Desarrollo')
    return render_template('index.html', otra=name)