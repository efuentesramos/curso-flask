from flask import Flask

from my_app.tasks.controller import taskRoute

from my_app.config import DevConfig

app = Flask(__name__)
app.register_blueprint(taskRoute)

app.config.from_object(DevConfig)