### Author: Carlos Gutierrez

import webapp2

from google.appengine.ext import db
from django.utils import simplejson as json

class Vehicle(db.Model):
	id = db.StringProperty()
	licplate = db.TextProperty()
	active = db.StringProperty()

class Vehicles(webapp2.RequestHandler):

	def getRequestData(self):
		self.current = {
			"id": self.request.get('id'), 
			"licplate": self.request.get('placas'), 
			"active": self.request.get('active'),
			"op": self.request.get('op')
		}

	def list(self):
		entries = db.GqlQuery("SELECT * FROM Vehicle ORDER BY id asc")
		items = []
		for entry in entries: 
			items.append({"id" : entry.id, "licence_plates" : entry.licplate, "active" : entry.active})
		json.dump({"vehicles": items}, self.response.out)
		
	def save(self):
		self.getRequestData()
		id = self.current["id"]
		licplate = self.current["licplate"]
		active = self.current["active"]
		flag = True
		if self.current["op"] == "create" and not licplate:
			flag = False
		if id and flag:
			entry = db.GqlQuery("SELECT * FROM Vehicle where id = :1", id).get()
			if not active:
				active = "true"
			if entry:
				if licplate:
					entry.licplate = licplate
				entry.active = active
			else:
				entry = Vehicle(id = id, licplate = licplate, active = active)
			entry.put()
			json.dump({"result": "ok"}, self.response.out)
		else:
			json.dump({"result": "missing parameters"}, self.response.out)
			
	def delete(self):
		id = self.request.get('id')
		if id:
			entry = db.GqlQuery("SELECT * FROM Vehicle where id = :1", id).get()
			if entry:
				db.delete(entry)
				json.dump({"result": "ok"}, self.response.out)
			else:
				json.dump({"result": "not found"}, self.response.out)
		else:
			json.dump({"result": "missing parameters"}, self.response.out)
			
	def getItem(self):
		id = self.request.get('id')
		if id:
			entry = db.GqlQuery("SELECT * FROM Vehicle where id = :1", id).get()
			if entry:
				json.dump({"id" : entry.id, "licence_plates" : entry.licplate, "active" : entry.active}, self.response.out)
			else:
				json.dump({"result": "not found"}, self.response.out)
		else:
			json.dump({"result": "missing parameters"}, self.response.out)
			
	def executeOp(self):
		op = self.request.get('op')
		if op:
			self.response.headers['Content-Type'] = 'application/json'	
			if op == "create":
				self.save()
			elif op == "update":
				self.save()
			elif op == "list":
				self.list()
			elif op == "delete":
				self.delete()
			elif op == "read":
				self.getItem()
			else:
				json.dump({"result": "unsupported command"}, self.response.out)
		else:
			json.dump({"result": "missing parameters"}, self.response.out)
		
	def get(self):
		self.executeOp()
		
	def post(self):
		self.executeOp()