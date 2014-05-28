### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

import webapp2
import time
from google.appengine.ext import db
from invoice import Invoice
from django.utils import simplejson as json

class InvoicesPhone(webapp2.RequestHandler):

	def store_a_value(self, tag, value):
		try:
			config = json.loads(value)
			id = self.getLastKey()+1
			id_driver = str(config["id_con"])
			id_vehicle = str(config["id_veh"])
			id_dispatcher = str(config["id_des"])
			id_gasStation = str(config["id_gas"])
			gas = str(config["litros"])
			total = str(config["total"])
			date = time.strftime("%d/%m/%Y")
			code = str(id) + id_driver + id_vehicle + id_dispatcher + id_gasStation
			entry = Invoice(id = id, id_driver = id_driver, id_vehicle = id_vehicle, id_dispatcher = id_dispatcher, id_gasStation = id_gasStation, code = code, date = date, gas=gas, total = total)
			entry.put()
			value = code
		except:
			value = "Error:"+value
		
		if self.request.get('fmt') == "html":
			json.dump({"result": True, "message": value}, self.response.out)
		else:
			self.WriteToPhoneAfterStore(self,tag,value)
		
	def doRequest(self):
		tag = self.request.get('tag')
		value = self.request.get('value')
		self.store_a_value(tag, value)
		
	def WriteToPhoneAfterStore(self, handler,tag, value):
		handler.response.headers['Content-Type'] = 'application/jsonrequest'
		json.dump(["STORED", tag, value], handler.response.out)
		
	def getLastKey(self):
		id = 0
		obj = db.GqlQuery("SELECT * FROM Invoice ORDER BY id DESC").get()
		if obj and obj.id:
			id = obj.id
		return id
	
	def get(self):
		self.doRequest()
		
	def post(self):
		self.doRequest()