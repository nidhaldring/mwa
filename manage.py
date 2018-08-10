from app import create_app,db
from flask_script import Manager
from app.models import User,Role
app=create_app("default")
manager=Manager(app)

@manager.shell
def _mk_():
    return dict(app=app,db=db,User=User,Role=Role)

if __name__=="__main__":
    manager.run()

