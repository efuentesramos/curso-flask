from flask import Flask, render_template, request

from my_app.tasks.controller import taskRoute

from my_app.config import DevConfig

app = Flask(__name__)
app.register_blueprint(taskRoute)

app.config.from_object(DevConfig)

@app.route('/')
def hello_world():
    name = request.args.get('name','Desarrollo')
    return render_template('index.html', otra=name)