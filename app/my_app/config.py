class Config(object):
    pass

class prodConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:admin@localhost:3306/tasks"

