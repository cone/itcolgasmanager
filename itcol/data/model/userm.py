### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

from google.appengine.ext import db

class Userm(db.Model):
	id = db.IntegerProperty()
	name = db.TextProperty()
	user = db.TextProperty()
	password = db.TextProperty()

	
class Fields:
	mappings = {
		"id":"clave",
		"name":"nombre",
		"user":"usuario",
		"password":"contra"
	}
	root ="Usuarios"