#import api
class Transportation:
	TRAVEL_CONST_FACTOR = -1
	def __init__(self, time, start_lat, start_lng, end_lat, end_lng):
		self.time = time
		self.start_lat = start_lat
		self.start_lng = start_lng
		self.end_lat = end_lat
		self.end_lng = end_lng
		self.duration = api.pollHereTravelTime(start_lat, start_lng, end_lat, end_lng)
    
	def value(self):
		return TRAVEL_CONST_FACTOR * self.duration

class Attraction:
	def __init__(self, name, lat, lng, category, rating):
		self.name = name
		self.lat = lat
		self.lng = lng
		self.type = category
		self.rating = rating
	def duration(self):
		return 60
	def value(self, prev):
		return -5 + rating