from app.auth import auth
from app import loginmanager
from flask_login import login_required 
from app.forms import RegisterForm,LoginForm
from flask import render_template,request,url_for,redirect,flash,current_app
from app.models import User
from app import db
from app.auth.func import send_conf_mail
from flask_login import current_user
from flask_login import login_user,logout_user
from itsdangerous import SignatureExpired
from app.decorators import for_anonymous


@auth.route("/test")
@login_required
def test():
    return "ok"

@auth.route("/")
def index():
    return render_template("auth/index.html")


@auth.route("/register",methods=["POST","GET"])
@for_anonymous
def register():
    form=RegisterForm(request.form)
    if form.validate_on_submit():
        # it's a post request
       #check if user is in db or nah
       msg="user aldready taken"
       u=User.query.filter_by(username=form.username.data).first()
       if u is None:
          u=User.query.filter_by(email=form.email.data).first()
          msg="email already taken !"
       if u : # in both cases    
           flash(msg) # only one of them ; or else i'll be giving so much information about my users :)
           return redirect(url_for("auth.register"))
           # fuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuck
       u=User(username=form.username.data,
               password=form.password.data,
               email=form.email.data,
               gender=form.gender.data
               )
       try:
            db.session.add(u)
            db.session.commit()
            #due to me loggin users before the end of the request 
       except Exception as e:
           db.session.rollback()
           #flash("we've encoutred an error with the db please try later !")
           # no point if i'm raising after i guess !
           raise e
        #confirmation link sending here   
       
       send_conf_mail(u.email,u.generate_confirmation_link()) 
       ######

       flash(" Hey, an email has been sent to you , please follow the instructions !")   
       login_user(u)
       return render_template("auth/index.html")
    #if a get request however then ;
    flash("please register")
    return render_template("auth/register.html",form=form)


@auth.route("/login",methods=['POST','GET'])
@for_anonymous
def login():
    form=LoginForm(request.form)
    if form.validate_on_submit():
        u=User.query.filter_by(username=form.username.data,password=form.password.data).first()
        if u :
            login_user(u,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.index'))  
        flash("error ! please try again !")
        return redirect(url_for('auth.login'))
    return render_template("auth/login.html",form=form)    



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("successfully logged out , bye <3 ")
    return render_template("auth/index.html")




@auth.route("/confirm/<string:s>")
@login_required
def confirm(s):
    try:
        s=current_user.check_confirmation_token(s) 
    except SignatureExpired:
        flash(" the token has been expired !")
    except  Exception as e:
        flash(" BAD TOKEN ! please try again ")  
        raise e 
       

    if s :
        # if all is fine and no errors occured
        # althou i think i can do this with session.get('_flashed')
        # but nevermind for now
        flash("we're happy to have you ! welcome to our family :)")    
    return render_template("auth/index.html")    

@auth.route("/confirm")
@login_required
def resend_confirmation(): 
    # resending ...
    send_conf_mail(current_user.email,current_user.generate_confirmation_link())
    # dunt thinko
    flash(" a link has been sent again to your email , please check to complete your registration") 
    return render_template("auth/index.html")
           

@loginmanager.user_loader
def load(_id):
    return User.query.get(_id)
