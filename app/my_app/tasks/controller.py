import os
from flask import Blueprint,render_template,request,redirect,url_for

from werkzeug.utils import secure_filename

from my_app.tasks import operations
from my_app.tasks import forms

from my_app import config,app

taskRoute = Blueprint('task',__name__,url_prefix='/tasks')

@taskRoute.route('/')
def index():
    
    return render_template('dashboard/task/index.html', tasks=operations.getAll())

@taskRoute.route('/<int:id>')
def show(id:int):
    return'Show '+str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    operations.delete(id)
    return redirect(url_for('task.index'))

@taskRoute.route('/create',methods=('GET','POST'))
def create():
    #task= request.form.get('task')
    form = forms.Task()

    if form.validate_on_submit():
        print(form.name.data)
        operations.create(form.name.data)
        
    return render_template('dashboard/task/create.html',form=form)

@taskRoute.route('/update/<int:id>',methods=['GET','POST'])
def update(id:int):

    task= operations.getById(id,True)
    form = forms.Task()

    if request.method == 'GET':
        form.name.data = task.name

    if form.validate_on_submit():
        operations.update(id, form.name.data)
        print(form.file.data)
        print(form.file.data.filename)
        f= form.file.data
        if f and config.allowed_extensions_files(f.filename):
            
            filename=secure_filename(f.filename)
            f.save(os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'],filename))
        return redirect(url_for('task.index'))
        

    return render_template('dashboard/task/update.html',form=form , id=id)