

from app.main import main
from app.models import User
from flask import abort,render_template,redirect,url_for,flash
from flask_login import login_required,current_user
from app.forms import EditProfileForm,UploadForm
from flask import request
from app import db 
from flask import current_app
from app.auth.func import send_conf_mail
from werkzeug.utils import secure_filename
import os 


@main.route("/")
def index():
	return "hello"



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
			# hope this works 
			# if not than i need to see where current_user can be used
			#change the user state to uncofrmed
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


@main.route("/uploadprofilepicture",methods=['POST','GET'])
@login_required
def upload_pic():
	form=UploadForm(request.form)
	if form.validate_on_submit():
		if  not request.files:
			return redirect(url_for('.upload_pic'))
		filename=secure_filename(form.image_name.data)
		# so secure name basically removes / or \  depending on os 
		# to prevent vulnerabilities 
		#no need to check for extensions since it's done in the form submission 
		file=request.files[form.image_name.data]
		f=os.path.join(current_app['UPLOAD_FOLDER'],filename)	
		file.save(f)
		current_user.profile_pic=f
		db.session.add(current_user )
		flash("your profile pciture has been updated properly ")
		return redirect(url_for('.index'))