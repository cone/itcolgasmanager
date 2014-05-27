### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

from google.appengine.ext import db

class Vehicle(db.Model):
	id = db.IntegerProperty()
	brand = db.TextProperty()
	model = db.TextProperty()
	licplate = db.TextProperty()
	type = db.StringProperty()
	active = db.StringProperty()
	gas = db.StringProperty()
	
class Fields:
	mappings = {
		"id":"clave",
		"brand":"marca",
		"model":"modelo",
		"licplate":"placas",
		"type":"tipo",
		"active":"estatus",
		"gas":"litros"
	}
	root ="Vehiculos"
	