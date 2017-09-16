import json
from .models import Crowdedness

class _db(object):
	def store(self, data):
		# str = self.getStr(data)
		# j = json.loads(str)
		j = data
		if self.check(j):
			ret = self.check_exist(j)
			if ret:
				ret.crowdedness = j["crowdedness"]
				ret.save()
				return "Data updated\n"
			else:
				self._store(j)
				return "Data stored\n"
		else:
			return "data must contain 'lat', 'lng', 'crowdedness' and 'type'\n"


	# def getStr(self, data):
	# 	return list(data.items())[0][0]

	def check(self, j):
		keys = ['nameStr', 'lat', 'lng', 'crowdedness', 'type']
		return sum(list(map(lambda k: k in j, keys))) == len(list(j.items()))

	def check_exist(self, j):
		try:
			ret = Crowdedness.objects.get(nameStr=j['nameStr'])
			return ret
		except Exception:
			return False

	def _store(self, j):
		c = Crowdedness(nameStr=j['nameStr'].lower(), name=j['nameStr'], lat=j['lat'], lng=j['lng'], crowdedness=j['crowdedness'], type=j['type'])
		c.save()