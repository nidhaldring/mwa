

from app.main import main
from app.models import User
from flask import abort,render_template,redirect,url_for,flash
from flask_login import login_required,current_user
from app.forms import EditProfileForm
from flask import request
from app import db 
from flask import current_app,request
from app.auth.func import send_conf_mail
from werkzeug.utils import secure_filename
import os 
from os.path import splitext
from itsdangerous import Signer

@main.route("/")
def index():
	return render_template("auth/index.html")



@main.route("/user/<int:id>")
def profile(id):
	u=User.query.get(id)
	if not u:
		abort(404)	
	return render_template("main/user.html",user=u)	

# 
# think of a better way :/
@main.route("/edit",methods=["POST","GET"])
@login_required
def editprofile():
	form=EditProfileForm(request.form)
	if form.validate_on_submit():
		current_email=current_user.email
		##### {...}
		for field in form:
			if field.data is  not '' and field.name not in ('csrf_token','repassword','password'):
				setattr(current_user,field.name,field.data)

		if current_email != form.email.data:
			#in case the mail changed
			# gotta send dat conf email again
			#
			send_conf_mail(form.email.data,current_user.generate_confirmation_link())
			# 
			# 
			#change the user state to uncofirmed
			current_user.confirmed=False	
			flash("a message has been sent to your new email , please follow for instructions")
		
		#save changes 	
		db.session.add(current_user)
	
		flash(" your account has been updated properly ")
		return redirect(url_for('.editprofile'))
	for field in form:
		if field.name not in ('csrf_token','repassword'):
			field.data=getattr(current_user,field.name)	

	return render_template("main/edit.html",form=form)		


@main.route("/updateprofilepicture",methods=['POST','GET'])
@login_required
def upload_pic():
	
	if request.method=="POST":
		if  'file' not  in request.files:
			flash(" please upload a file !")
			return redirect(url_for('.upload_pic'))	
		request.files['file'].filename=secure_filename(request.files['file'].filename)
		# so secure name basically removes / or \  depending on os 
		# to prevent vulnerabilities 
		file=request.files['file']

		#checks file extension
		if splitext(file.filename)[1][1:] not in current_app.config['ALLOWED_EXTENSIONS']:
			flash("extension not allowed only %s ,%s, %s are allowed"%current_app.config['ALLOWED_EXTENSIONS'])
			return redirect(url_for('.upload_pic'))

		#every pic should have a unique name 
		split=list(splitext(file.filename))
		split[0]=Signer(current_app.config['SECRET_KEY']).sign(split[0].encode('utf-8')).decode('utf-8')
		file.filename="".join(split)
		#
		 
		path=os.path.join(current_app.config['UPLOAD_FOLDER'],file.filename)	

		# delete the old one
		if current_user.profile_pic != current_app.config["USER_DEFAULT_PIC"]:
			os.unlink(url_for('static',filename=current_user.profile_pic))

		current_user.profile_pic=path
		_=os.path.join('app','static')
		file.save(os.path.join( _ , path ))		
		#

		db.session.add(current_user )
		flash("your profile pciture has been updated properly ")
		return redirect(url_for('.index'))
	return render_template("main/upload.html")	

