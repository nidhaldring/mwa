from flask import Blueprint

auth=Blueprint("auth",__name__) # check if you can change template folder later :))))
from app.auth import views,errors
