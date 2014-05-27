### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

from google.appengine.ext import db

class GasStation(db.Model):
	id = db.IntegerProperty()
	name = db.TextProperty()
	street = db.TextProperty()
	colony = db.TextProperty()
	rs = db.TextProperty()
	phone = db.TextProperty()
	
class Fields:
	mappings = {
		"id":"clave",
		"name":"nombre",
		"street":"calle",
		"colony":"colonia",
		"rs":"razon_social",
		"phone":"tel"
	}
	root ="Gasolineras"