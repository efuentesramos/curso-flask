from my_app import db


class Task (db.Model):
    __tablename__='tasks'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    
    
    def _init_(self, name):
        self.name = name
        