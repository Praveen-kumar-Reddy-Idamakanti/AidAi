from database import db
import bcrypt

class User(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    type = db.StringField(required=True, choices=['donor', 'ngo', 'admin'])
    preferences = db.ListField(db.StringField())
    location = db.StringField()
    additionalInfo = db.StringField()
    avatar = db.StringField(default='/placeholder.svg')
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        
    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email).first()
        
    @classmethod
    def find_by_id(cls, id):
        return cls.objects(id=id).first()