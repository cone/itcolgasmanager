### Author: Carlos Gutierrez 
### EMail: coneramu@gmail.com

from abc import ABCMeta, abstractmethod
from django.utils import simplejson as json
from google.appengine.ext import db

class AbstactDAO:
	__metaclass__ = ABCMeta
	
	msgHash = {
		'SAVE_SUCCESS':'Registro creado satisfactoriamente.',
		'UPDATE_SUCCESS':'Registro actualizado satisfactoriamente.',
		'DELETE_SUCCESS':'Registro borrado satisfactoriamente.',
		'DUPLICATE_KEY':'Error: clave duplicada.',
		'MISSING_PARAMS':'Hacen falta parametros.',
		'NOT_FOUND':'Registro no encontrado.',
		'UNSUPPORTED':'Operacion no soportada.',
		'GENERIC_ROOT':'datos'
	}
	
	@abstractmethod
	def list(self):pass
	
	@abstractmethod
	def create(self):pass
	
	@abstractmethod
	def update(self):pass
	
	@abstractmethod
	def delete(self):pass
	
	@abstractmethod
	def getItem(self):pass
	
	@abstractmethod
	def executeOp(self):pass
	
	@abstractmethod
	def getTableName(self):pass
	
	def getRequestData(self):
		self.current = {}
		for key in self.mappings:
			self.current[key] = self.request.get(self.mappings[key]).strip()
		self.current["op"] = self.request.get("op")
		return self.current
		
	def getOutputJsonObj(self, entry):
		return self.getExternalOutputJsonObj(entry, self.mappings)
		
	def getExternalOutputJsonObj(self, entry, mappings):
		outputJson = {}
		for key in mappings:
			outputJson[mappings[key]] = getattr(entry, key)
		return outputJson
		
	def loadModelObj(self, entry, params):
		for key in self.mappings:
			if params[key]:
				setattr(entry, key, params[key])
		return entry
		
	def getLastKey(self):
		id = 0
		obj = db.GqlQuery("SELECT * FROM "+self.getTableName()+" ORDER BY id DESC").get()
		if obj and obj.id:
			id = obj.id
		return id
		
	def isNumber(self, numStr):
		try:
			float(numStr)
			return True
		except ValueError:
			return False
			
	def convertToInteger(self, str):
		if self.isNumber(str):
			return int(str)
		else:
			return 0
			
	#For the developing phase only
	def deleteAll(self):
		entries = db.GqlQuery("SELECT * FROM "+self.getTableName())
		for entry in entries: 
			db.delete(entry)
		json.dump({"result": True, "message":"Deleted."}, self.response.out)
	
	def executeOp(self):
		op = self.request.get('op')
		if op:
			self.response.headers['Content-Type'] = 'application/json'	
			if op == "create":
				self.create()
			elif op == "update":
				self.update()
			elif op == "list":
				self.list()
			elif op == "delete":
				self.delete()
			elif op == "read":
				self.getItem()
			elif op == "deleteall":
				self.deleteAll()
			else:
				json.dump({"result": False, "message":self.msgHash['UNSUPPORTED']}, self.response.out)
		else:
			json.dump({"result": False, "message":self.msgHash['MISSING_PARAMS']}, self.response.out)