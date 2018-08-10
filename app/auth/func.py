from flask_mail import Message
from flask import current_app as app
from app import mail 

def send_conf_mail(recp,conf_link):
	msg=Message(recipients=[recp])
	msg.body="welcome to our website, please follow the link bellow to finish registering  :)  (love) "+conf_link
	with app.app_context():
		mail.send(msg)
		#done

