### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

import webapp2

from google.appengine.ext import db
from django.utils import simplejson as json
from invoice import Invoice
from invoice import Fields
from vehicle import Fields as vehicleFields
from driver import Fields as driverFields
from dispatcher import Fields as dispatcherFields
from gasStation import Fields as gasStationFields
from abstract import AbstactDAO

class Invoices(webapp2.RequestHandler, AbstactDAO):

	mappings = Fields.mappings

	def list(self):
		params = self.getRequestData()
		if params['date']:
			entries = db.Query(Invoice).filter('date', params['date'])
			#entries = db.GqlQuery("SELECT * FROM Invoice where date = :1", params['date'])
		else:
			entries = db.GqlQuery("SELECT * FROM Invoice")
		items = []
		for entry in entries: 
			items.append(self.merge(entry))
		json.dump({Fields.root: items}, self.response.out)
		
	def create(self):
		params = self.getRequestData()
		if params['id_driver'] and params['id_vehicle'] and params['id_dispatcher'] and params['id_gasStation'] and params['date']:
			params['id'] = self.getLastKey()+1
			id = params['id']
			params['code'] = str(id) + params['id_driver'] + params['id_vehicle'] + params['id_dispatcher'] + params['id_gasStation']
			entry = self.loadModelObj(Invoice(), params)
			entry.put()
			json.dump({"result": True, "message":self.msgHash['SAVE_SUCCESS']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def update(self):
		params = self.getRequestData()
		if params['id']:
			entry = db.GqlQuery("SELECT * FROM Invoice where id = :1", self.convertToInteger(params['id'])).get()
			if entry:
				params['id'] = self.convertToInteger(params['id'])
				entry = self.loadModelObj(entry, params)
			else:
				json.dump({"result": False, "message":self.msgHash['NOT_FOUND']}, self.response.out)
				return
			entry.put()
			json.dump({"result": True, "message":self.msgHash['UPDATE_SUCCESS']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def delete(self):
		params = self.getRequestData()
		if params['id']:
			params['id'] = self.convertToInteger(params['id'])
			entry = db.GqlQuery("SELECT * FROM Invoice where id = :1", params['id']).get()
			if entry:
				db.delete(entry)
				json.dump({"result": True, "message":self.msgHash['DELETE_SUCCESS']}, self.response.out)
			else:
				json.dump({"result": False, "message":self.msgHash['NOT_FOUND']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def getItem(self):
		params = self.getRequestData()
		if params['id']:
			params['id'] = self.convertToInteger(params['id'])
			entry = db.GqlQuery("SELECT * FROM Invoice where id = :1", params['id']).get()
			if entry:
				json.dump(self.merge(entry), self.response.out)
			else:
				json.dump({"result": False, "message":self.msgHash['NOT_FOUND']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def merge(self, entry):
		#App engine mongo db does no support JOIN
		aux = {}
		aux[self.msgHash['GENERIC_ROOT']] = self.getOutputJsonObj(entry)
		vehicle = db.GqlQuery("SELECT * FROM Vehicle where id = :1", self.convertToInteger(entry.id_vehicle)).get()
		if vehicle:
			aux[vehicleFields.root] = self.getExternalOutputJsonObj(vehicle, vehicleFields.mappings)
		driver = db.GqlQuery("SELECT * FROM Driver where id = :1", self.convertToInteger(entry.id_driver)).get()
		if driver:
			aux[driverFields.root] = self.getExternalOutputJsonObj(driver, driverFields.mappings)
		dispatcher = db.GqlQuery("SELECT * FROM Dispatcher where id = :1", self.convertToInteger(entry.id_dispatcher)).get()
		if dispatcher:
			aux[dispatcherFields.root] = self.getExternalOutputJsonObj(dispatcher, dispatcherFields.mappings)
		gasStation = db.GqlQuery("SELECT * FROM GasStation where id = :1", self.convertToInteger(entry.id_gasStation)).get()
		if gasStation:
			aux[gasStationFields.root] = self.getExternalOutputJsonObj(gasStation, gasStationFields.mappings)
		return aux
		
	def getTableName(self):
		return "Invoice"
		
	def get(self):
		self.executeOp()
		
	def post(self):
		self.executeOp()