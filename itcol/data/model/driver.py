### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

from google.appengine.ext import db

class Driver(db.Model):
	id = db.IntegerProperty()
	name = db.TextProperty()
	rfc = db.TextProperty()
	phone = db.TextProperty()
	
class Fields:
	mappings = {
		"id":"clave",
		"name":"nombre",
		"rfc":"rfc",
		"phone":"tel"
	}
	root ="Conductores"
	