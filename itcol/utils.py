class Utils:
	@staticmethod
	def toOutDict(fields, entry):
		dict = {}
		for key in fields:
			dict[fields[key]] =  entry[key]
		return dict