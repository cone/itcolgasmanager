### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

from google.appengine.ext import db

class Invoice(db.Model):
	id = db.IntegerProperty()
	id_driver = db.StringProperty()
	id_vehicle = db.StringProperty()
	id_dispatcher = db.StringProperty()
	id_gasStation = db.StringProperty()
	code = db.TextProperty()
	gas = db.TextProperty()
	total = db.TextProperty()
	date = db.TextProperty()
	
class Fields:
	mappings = {
		"id":"clave",
		"id_driver":"id_con",
		"id_vehicle":"id_veh",
		"id_dispatcher":"id_des",
		"id_gasStation":"id_gas",
		"code":"codigo",
		"gas":"litros",
		"total":"total",
		"date":"fecha"
	}
	root ="Facturas"