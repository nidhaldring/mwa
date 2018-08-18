from flask_wtf import Form
from wtforms import ValidationError
from wtforms import StringField,PasswordField,RadioField,TextField,BooleanField,FileField
from wtforms.validators import DataRequired,EqualTo,Email,Length,Regexp
import string
from flask import current_app


class RegisterForm(Form):
    username=StringField("write your name plz ",[DataRequired(message="username can't be left blank"),Length(4,69)])
    password=PasswordField("write your password",[DataRequired(message=" password can't be left blank"),Length(4,120,message="password must be more than 4 ")])
    repassword=PasswordField("rewrite your  password",[DataRequired(),EqualTo("password",message="passwords dosn't match")])   
    email=StringField("write your mail here",[DataRequired(),Email()])
    gender=RadioField("choose your gender",choices=[("male","male"),("female","female"),("other","other")])
    about_me=TextField("write smthng that describes you :) ")
    def validate_password(form,field):
        i=False
        for j in string.punctuation:
            if j in field.data:
                i=True
                break       
        if not i:
            raise ValidationError("password must at least contain one special character")
        #this checks that  tada there -> (90)    



class LoginForm(Form):
    username=StringField("please write your username ",[DataRequired()]) 
    password=PasswordField("please write your password",[DataRequired()])
    remember_me=BooleanField("remember me ?",default=True)       
        

class EditProfileForm(Form):
    username=StringField("name please",[Length(4,69)])
    password=PasswordField("write your password ")
    repassword=PasswordField("rewrite your password",[EqualTo("password",message="passwords don't match")])
    email=StringField("email please",[Email()])
    gender=StringField()
    about_me=TextField()
    # i do beleive now that there's no point letting the admins choose an invalid email

    #since i can't show password on the form i'm supposed to validate its length here
    def validate_password(form,field):
        if field.data is not '' and (len(field.data)> 4 and len(field.data)<120) is not True : 
            raise ValidationError("password should be between 4 to 100 caracters")


#might as well finish writing better error messages     



    