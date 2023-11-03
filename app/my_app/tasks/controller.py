from flask import Blueprint,render_template,request,redirect,url_for

taskRoute = Blueprint('task',__name__,url_prefix='/tasks')

task_list =['task 1','task 2','task 3']

@taskRoute.route('/')
def index():
    return render_template('dashboard/task/index.html', tasks=task_list)

@taskRoute.route('/<int:id>')
def show(id:int):
    return'Show '+str(id)

@taskRoute.route('/delete/<int:id>')
def delete(id:int):
    del task_list[id]

    return redirect(url_for('task.index'))

@taskRoute.route('/create',methods=('GET','POST'))
def create():
    task= request.form.get('task')
    if task!=None:
        task_list.append(task)
        return redirect(url_for('task.index'))
        
    return render_template('dashboard/task/create.html')

@taskRoute.route('/update/<int:id>',methods=['GET','POST'])
def update(id:int):

    task= request.form.get('task')
    if task!=None:
        task_list[id]= task

    return render_template('dashboard/task/update.html')