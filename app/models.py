
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as serial,SignatureExpired,BadSignature


class PERMISSION:
    WRITE_COMMENT=1
    WRITE_POSTS=10
    MODERATE=100
    ADMIN=1000


#
class AnonymousUser:
    @property
    def is_active(self):
        return False
    @property
    def is_anonymous(self):
        return True 
    @property 
    def is_authenticated(self):
        return False 
    def get_id(self):
        return None    
    def can(self,perm):
        return False 
    def is_admin(self):
        return False       

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(69),unique=True)
    password=db.Column(db.String(138))
    email=db.Column(db.String(69),unique=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    gender=db.Column(db.String(10))
    confirmed=db.Column(db.Boolean,default=False)
    about_me=db.Column(db.Text,nullable=True)
    profile_pic=db.Column(db.Text,default='def.jpg')

    def __init__(self,**kargs):
        # yup now i know wut does this super line does :/ 
        # learned it the hard way 
        super().__init__(**kargs) # *** never forget 
        self.s=None

    #FOR FLASK LOGIN
    @property
    def is_active(self):
        return True
    @property
    def is_authenticated(self):
        return True # might require some working later :) 
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

    # security stuff
    def generate_confirmation_link(self):
        self.s=serial(current_app.config["SECRET_KEY"],expires_in=24*3600) # by default expires in 24 h  
        return "http://127.0.0.1:5000/auth/confirm/"+str(self.s.dumps({'id':self.id}))
        #
    def check_confirmation_token(self,token):
        if self.s.loads(token).get('id') == self.id :
            self.confirmed=True
            db.session.add(self)
        else :
            raise Exception    
            # base  will work 
        # if all is fine 
        return True    
          
    def can(self,perm):
        return self.perm&perm==perm  
    def is_admin(self):
        return PERMISSION.ADMIN&self.perm==PERMISSION.ADMIN    



class Role(db.Model):
    __tablename__="roles"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(69),unique=True)
    users=db.relationship(User,backref="role",lazy=True)





