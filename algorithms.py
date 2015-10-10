#! /usr/bin/env python

import requests
import time
import random

class LatLng:
	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng

	def dist_to(self, latlng):
		return distance(self.lat, self.lng, latlng.lat, latlng.lng)

	def __str__(self):
		return "(%f,%f)" % (self.lat, self.lng)

	def distance(start_lat, start_lng, end_lat, end_lng):
		# Found at http://www.geodatasource.com/developers/javascript and modified
		# Units: miles
		radlat1 = math.pi * start_lat / 180
		radlat2 = math.pi * end_lat / 180
		radlng1 = math.pi * start_lng / 180
		radlng2 = math.pi * end_lng / 180
		theta = end_lng - start_lng
		radtheta = math.pi * theta / 180

		dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta);
		dist = math.acos(dist)
		dist = dist * 180 * 60 * 1.1515 / math.pi
		return dist

	def to_json(self):
		return '{ "lat": %f, "lng": %f}' % (self.lat, self.lng)


class ItineraryEvent:
	TRAVEL_CONST = -1
	def __init__(self, name, lat, lng, category, rating, origin, travel_time):
		self.name = name
		self.lat = lat
		self.lng = lng
		self.position = LatLng(lat, lng)
		self.cat = category
		self.base_score = rating
		self.origin = origin
		self.travel_time = travel_time

	def duration(self):
		return 7200

	def value(self, prev):
		score = self.base_score - 5
		score += ItineraryEvent.TRAVEL_CONST * self.travel_time/3600
		return score

	def update_origin(self, orig):
		self.origin = orig
		self.travel_time = pollHereTravelTime(orig.lat, orig.lng, self.lat, self.lng)

	def to_json(self):
		return '{"type": "transportation", "start":%s, "end":%s}, ' % (self.origin.to_json(), self.position.to_json()) + \
		'{"type":"attraction","position": %s, "name": "%s", "cat": "%s"}' % (self.position.to_json(), self.name, self.cat)

	def __str__(self):
		return "{'name': '%s', 'cat': '%s', 'rating': %f}" % (self.name, self.cat, self.base_score)

def jsonify(itinerary, end):
	return '[' + ",".join(map(lambda x:x.to_json(), itinerary)) + \
		',{"type": "transportation", "start":%s, "end":%s}]' % (itinerary[-1].position.to_json(), end.to_json())

def score(itinerary):
	score = 100.0
	events = []
	for evt in itinerary:
		score += evt.value(events)
	return score

def build_itinerary(act_list, start, end):
	itinerary = []
	while len(act_list) > 0:
		for i in act_list:
			i.update_origin(start)
		act_list.sort(key=lambda x: x.travel_time, reverse = True)
		itinerary.append(act_list.pop())
		start = itinerary[-1].position
	return itinerary

def pollHereTravelTime(a, b, c, d):
	#start = time.clock()
	a,b,c,d = map(str, [a,b,c,d])
	url = "https://route.cit.api.here.com/routing/7.2/calculateroute.json?waypoint0=" + a + "%2C" + b + "&waypoint1=" + c + "%2C" + d + "&mode=fastest%3Bcar%3Btraffic%3Aenabled&app_id=N6MJW6UzW079S5ZZwcPl&app_code=FOkZLbFrMx77dDpomCs9ZQ&tf&departure=now"
	r = requests.get(url)
	relevant = r.json()
	#print time.clock() - start
	return relevant["response"]["route"][0]["summary"]["travelTime"]


def pollHereAttractions(a, b):
	#start = time.clock()
	response = []
	url = "http://places.cit.api.here.com/places/v1/discover/explore%20?at=" + str(a) + "," + str(b) + ";r=20000&cat=sights-museums,leisure-outdoor,natural-geographical,going-out&app_id=N6MJW6UzW079S5ZZwcPl&app_code=FOkZLbFrMx77dDpomCs9ZQ&tf=plain"
	r = requests.get(url)
	relevant = r.json()["results"]["items"]
	for x in range(len(relevant)):
		name = relevant[x]["title"]
		category = relevant[x]["category"]["title"]
		location = relevant[x]["position"]
		rating = relevant[x]["averageRating"]
		response.append(ItineraryEvent(name,location[0], location[1], category, rating, 0, 0))
	#print time.clock() - start
	return response

def test():
	overall_start = time.clock()
	print (overall_start)
	timer_start = time.clock()
	shortlist = pollHereAttractions(52.5160,13.3779)
	print ("Get Attractions: %f" % (time.clock() - timer_start))
	inds = range(len(shortlist))
	random.shuffle(inds)
	act_list = [shortlist[k] for k in inds[:5]]
	timer_start = time.clock()
	i = build_itinerary(act_list, LatLng(52.5160,13.3779), LatLng(52,13))
	print ("Build Itinerary: %f" % (time.clock() - timer_start))
	timer_start = time.clock()
	print (score(i))
	print (jsonify(i, LatLng(52,14)))

def get_best_itinerary(start_lat, start_lng, end_lat, end_lng):
	start = LatLng(start_lat, start_lng)
	end = LatLng(end_lat, end_lng)
	all_attractions = pollHereAttractions(start.lat, start.lng)
	best_score = 0
	best_itinerary = "[]"

	for i in range (20):
		inds = range(len(all_attractions))
		random.shuffle(inds)
		shortlist = [all_attractions[i] for i in inds[:4]]
		itn = build_itinerary(shortlist, start, end)
		itn_score = score(itn)
		if itn_score > best_score:
			best_score = itn_score
			best_itinerary = jsonify(itn,end)
		return best_itinerary


