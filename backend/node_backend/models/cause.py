from backend.python_backend.database import db

class Cause(db.Document):
    name = db.StringField(required=True)
    organization = db.StringField(required=True)
    description = db.StringField(required=True)
    image = db.StringField(default='/placeholder.svg')
    goal = db.FloatField(required=True)
    raised = db.FloatField(default=0)
    tags = db.ListField(db.StringField())
    location = db.StringField(required=True)
    impact = db.StringField()
    donorCount = db.IntField(default=0)
    verified = db.BooleanField(default=False)
    blockchain = db.DictField()
    
    @classmethod
    def find_all(cls):
        return cls.objects.all()
        
    @classmethod
    def find_by_id(cls, id):
        return cls.objects(id=id).first()