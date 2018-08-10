from flask import abort,render_template,flash
from flask_login import current_user
from functools import wraps
# decorator that prohibit logged user from accessing a certain view

def for_anonymous(view):
	@wraps(view)
	def decorator(*args,**kargs):
		if  not current_user.is_anonymous:
			flash(" you need to log out to acess this page")
			return render_template("auth/index.html")
		return view(*args,**kargs)
	return decorator	



		
