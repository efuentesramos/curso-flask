import os

ALLOWED_EXTENSIONS_FILES = {'pdf','jpg','jpeg','git','png'}

def allowed_extensions_files(filename):
    return '.' in filename and filename.lower().rsplit('.',1)[1] in ALLOWED_EXTENSIONS_FILES

class Config(object):
    UPLOAD_FOLDER = os.path.realpath ('.') + '/app/my_app/uploads'


class prodConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:admin@localhost:3306/tasks"
    SECRET_KEY = 'SECRET_KEY'
    #WTF_CSRF_ENABLE = False

