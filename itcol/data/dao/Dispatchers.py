### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

import webapp2

from google.appengine.ext import db
from django.utils import simplejson as json
from dispatcher import Dispatcher
from dispatcher import Fields
from abstract import AbstactDAO

class Dispatchers(webapp2.RequestHandler, AbstactDAO):

	mappings = Fields.mappings

	def list(self):
		entries = db.GqlQuery("SELECT * FROM Dispatcher ORDER BY id asc")
		items = []
		for entry in entries: 
			items.append(self.getOutputJsonObj(entry))
		json.dump({Fields.root: items}, self.response.out)
		
	def create(self):
		params = self.getRequestData()
		if params['name']:
			params['id'] = self.getLastKey()+1
			entry = self.loadModelObj(Dispatcher(), params)
			entry.put()
			json.dump({"result": True, "message":self.msgHash['SAVE_SUCCESS']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def update(self):
		params = self.getRequestData()
		if params['id']:
			entry = db.GqlQuery("SELECT * FROM Dispatcher where id = :1", self.convertToInteger(params['id'])).get()
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
		id = self.convertToInteger(self.getRequestData()['id'])
		if id:
			entry = db.GqlQuery("SELECT * FROM Dispatcher where id = :1", id).get()
			if entry:
				db.delete(entry)
				json.dump({"result": True, "message":self.msgHash['DELETE_SUCCESS']}, self.response.out)
			else:
				json.dump({"result": False, "message":self.msgHash['NOT_FOUND']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def getItem(self):
		id = self.convertToInteger(self.getRequestData()['id'])
		if id:
			entry = db.GqlQuery("SELECT * FROM Dispatcher where id = :1", id).get()
			if entry:
				json.dump(self.getOutputJsonObj(entry), self.response.out)
			else:
				json.dump({"result": False, "message":self.msgHash['NOT_FOUND']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)
			
	def getTableName(self):
		return "Dispatcher"
		
	def get(self):
		self.executeOp()
		
	def post(self):
		self.executeOp()