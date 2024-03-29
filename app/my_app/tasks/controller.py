import os
from flask import Blueprint,render_template,request,redirect,url_for,flash

from flask_login import login_required

from werkzeug.utils import secure_filename

from my_app.tasks import operations,forms,models


from my_app.documents import operations as doc_operations

from my_app import config,app

taskRoute = Blueprint('task',__name__,url_prefix='/tasks')

@taskRoute.route('/')
@login_required
def index():
    
    return render_template('dashboard/task/index.html', tasks=operations.getAll())

@taskRoute.route('/<int:id>')
@login_required
def show(id:int):
    return'Show '+str(id)

@taskRoute.route('/delete/<int:id>')
@login_required
def delete(id:int):
    task=operations.getById(id,True)
    operations.delete(task.id)
    doc_operations.delete(task.document_id)
    return redirect(url_for('task.index'))

@taskRoute.route('/create',methods=('GET','POST'))
@login_required
def create():
    #task= request.form.get('task')
    form = forms.Task()
    form.category.choices = [(c.id, c.name) for c in models.Category.query.all()]

    if form.validate_on_submit():
        print(form.name.data)
        operations.create(form.name.data,form.category.data)
        
    return render_template('dashboard/task/create.html',form=form)

@taskRoute.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id:int):

    task= operations.getById(id,True)

    form = forms.Task()
    form.category.choices = [(c.id, c.name) for c in models.Category.query.all()]

    #tags
    formTag = forms.TaskTagAdd()
    formTag.tag.choices = [(t.id, t.name) for t in models.Tag.query.all()]

    formTagRemove = forms.TaskTagRemove()
    #tags


    if request.method == 'GET':
        form.name.data = task.name
        form.category.default = task.category_id
        

    if form.validate_on_submit():
        operations.update(id, form.name.data,form.category.data)
        
        f= form.file.data
        if f and config.allowed_extensions_files(f.filename):
            
            filename=secure_filename(f.filename)
            document = doc_operations.create(filename, filename.lower().rsplit('.',1)[1],f)

            operations.update(id, form.name.data,form.category.data, document.id)

        flash('The registry has been update succesfully','info')   
                        
        #return redirect(url_for('task.index'))
        

    return render_template('dashboard/task/update.html',form=form,formTag=formTag,formTagRemove=formTagRemove, task=task , id=id)

@taskRoute.route('/<int:id>/tag/add', methods=['POST'])
@login_required
def tagAdd(id:int):
    formTag = forms.TaskTagAdd()
    formTag.tag.choices = [(t.id, t.name) for t in models.Tag.query.all()]

    if (formTag.validate_on_submit()):
        operations.addTag(id,formTag.tag.data)
    
    return redirect(url_for('task.update', id=id))


@taskRoute.route('/<int:id>/tag/remove', methods=['POST'])
@login_required
def tagRemove(id:int):
    formTag = forms.TaskTagRemove()
    
    if (formTag.validate_on_submit()):
        operations.removeTag(id,formTag.tag.data)
    
    return redirect(url_for('task.update', id=id))