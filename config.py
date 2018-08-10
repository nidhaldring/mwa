import os


class Config:
	#ADMIN_MAIL="dringthedreamer@gmail.com"
    SECRET_KEY="@NIDHAL"
    TESTING=False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    UPLOAD_FOLDER="./uploads"
    
    #USELESS FOR NOW
    #lel berka :v
    def init_app(app):pass
    
class Dev(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)),"dev.sqlite")
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
    MAIL_USERNAME=os.environ.get("USERNAME")
    MAIL_PASSWORD=os.environ.get("PASSWORD")
    MAIL_DEFAULT_SENDER=("admin","dringthedreamer@gmail.com")
    MAX_CONTENT_LENGTH=16*1024*1024
    # 16 mb is the max for file uploading 


class Test(Dev):
    Testing=True
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)),"test.sqlite")

    
config=dict(default=Dev,Dev=Dev,Test=Test)
#ends here
