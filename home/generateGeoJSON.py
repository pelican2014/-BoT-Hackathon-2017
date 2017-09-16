import json

class _generateGeoJSON(object):
	def __init__(self, name, type, lat, lng, crowdedness):
		if not (len(lat) == len(lng) == len (crowdedness)):
			raise Exception("length not equal")
		self.lat = lat
		self.lng = lng
		self.crowdedness = crowdedness
		self.name = name
		self.type = type

	def makeFromSkeleton(self):
		j = {"type": "FeatureCollection", "features": []}
		for i in range(0, len(self.lat)):
			j["features"].append(self.makeForPush(i))
		return j

	def makeForPush(self, i):
		j = {}
		j["type"] = "Feature"
		j["properties"] = {"name": self.name[i], "crowdedness": self.crowdedness[i], "type": self.type[i]}
		j["geometry"] = {"type": "Point", "coordinates": [self.lng[i], self.lat[i]]}
		return j

	def get(self):
		return (json.dumps(self.makeFromSkeleton()), min(self.crowdedness), max(self.crowdedness))