#! /usr/bin/env python

import requests
import time
import json
import random
import math
import operator
import itertools

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

class LatLng:
	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng

	def dist_to(self, latlng):
		return distance(self.lat, self.lng, latlng.lat, latlng.lng)

	def __str__(self):
		return "(%f,%f)" % (self.lat, self.lng)

	def to_dict(self):
		return { "lat":self.lat, "lng": self.lng}

	def to_json(self):
		return json.dumps(self.to_json())

class Transportation:
	TRAVEL_CONST = -1

	def __init__(self, start, end, category, number, begin_time, duration):
		self.name = "transport%d" % number
		self.start = start
		self.end = end
		self.type = "transportation"
		self.cat = category
		self.begin_time = begin_time
		self.duration = duration

	@classmethod
	def init_null(cls):
		return cls({0,180},{0,180},"",-1,-1,-1)

	def update(self, start, end, category, number, begin_time):
		self.name = "transport%d" % number
		self.start = start
		self.end = end
		self.cat = category
		self.begin_time = begin_time

	def update_duration(self):
		self.duration = pollHereTravelTime(self.start.lat, self.start.lng, \
										   self.end.lat, self.end.lng)

	def to_dict(self):
		return {'name':self.name, \
		 'start': self.start.to_dict(), \
		 'end': self.end.to_dict(), \
		 'type': "transportation", \
		 'cat': self.cat, \
		 'duration': self.duration}

	def end_time(self):
		return self.begin_time + self.duration	 

	def to_json(self):
		return json.dumps(self.to_dict())

	def value(self, prev):
		return Transportation.TRAVEL_CONST * self.duration/3600
	
class Attraction:
	def __init__(self, name, position, category, rating):
		self.name = name
		self.position = position
		self.cat = category
		self.type = "attraction"
		self.base_score = rating
		self.transport = Transportation.init_null()
		self.start_time = 0

	def to_dict(self):
		return {'name':self.name, \
		 'position': self.position.to_dict(), \
		 'type': "attraction", \
		 'cat': self.cat}

	def to_json(self):
		return json.dumps(self.to_dict())

	def duration(self):
		return 7200

	def end_time(self):
		return self.start_time + self.duration()

	def total_time(self):
		return 7200 + self.transport.duration

	def update_transport(self, start, category, number, begin_time):
		self.transport.update(start, self.position, category, number, self.start_time)
		self.transport.update_duration()
		self.start_time += self.transport.duration

	def value(self, prev):
		return self.base_score - 5

def score(itinerary):
	score = 100.0
	events = []
	for evt in itinerary:
		score += evt.value(events)
	return score

def build_itinerary(act_list, start, end, start_time, end_time):
	curr_time = start_time
	itinerary = []
	transport_no = 1
	while len(act_list) > 0:
		for i in act_list:
			i.start_time = curr_time
			i.update_transport(start, "Uber", transport_no, curr_time)
		act_list.sort(key=lambda x: x.total_time(), reverse = True)
		next_act = act_list.pop()
		itinerary.append(next_act.transport)
		itinerary.append(next_act)
		start = next_act.position
		curr_time += next_act.total_time()
		transport_no += 1

	time_home = pollHereTravelTime(start.lat, start.lng, end.lat, end.lng)
	itinerary.append(Transportation(start, end, "Uber", transport_no, curr_time, time_home))
	return itinerary

def score(itinerary):
	score = 100.0
	events = []
	for evt in itinerary:
		score += evt.value(events)
	return score

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
		category = relevant[x]["category"]["id"]
		location = relevant[x]["position"]
		rating = relevant[x]["averageRating"]
		response.append(Attraction(name, LatLng(location[0],location[1]), category, rating))
	#print time.clock() - start
	return response

def pollHereAttractionsBox(start, end):
	west = min(start.lng, end.lng) - 0.0005
	east = max(start.lng, end.lng) + 0.0005
	south = min(start.lat, end.lat) - 0.0001
	north = max(start.lat, end.lat) + 0.0001
	bbox = ",".join(map(str, [west,south,east,north]))
	#start = time.clock()
	response = []
	url = "http://places.cit.api.here.com/places/v1/discover/explore%20?in=" + bbox + "&cat=sights-museums,leisure-outdoor,natural-geographical,going-out&app_id=N6MJW6UzW079S5ZZwcPl&app_code=FOkZLbFrMx77dDpomCs9ZQ&tf=plain"
	print url
	r = requests.get(url)
	relevant = r.json()["results"]["items"]
	for x in range(len(relevant)):
		name = relevant[x]["title"]
		category = relevant[x]["category"]["id"]
		location = relevant[x]["position"]
		rating = relevant[x]["averageRating"]
		response.append(Attraction(name, LatLng(location[0],location[1]), category, rating))
	#print time.clock() - start
	return response

def get_all_data(start_lat, start_lng, end_lat, end_lng, start_time, end_time, pin_list=[]):
	start = LatLng(start_lat, start_lng)
	end = LatLng(end_lat, end_lng)
	all_attractions = pollHereAttractionsBox(start,end)
	best_score = 0
	best_itinerary = []

	output = {}
	for i in range (3):
		inds = range(len(all_attractions))
		random.shuffle(inds)
		shortlist = [all_attractions[i] for i in inds[:3]]
		itn = build_itinerary(shortlist, start, end, 0, 3600 * 6)
		itn_score = score(itn)
		if itn_score > best_score:
			best_score = itn_score
			best_itinerary = itn

	activity_list = map(lambda x:x.to_dict(), all_attractions)
	itinerary = []
	for i in best_itinerary:
		itinerary.append({"name":i.name, "end_time":i.end_time()})
		if i.type=="transportation":
			activity_list.append(i.to_dict())

	output['activityList'] = activity_list
	output['itinerary'] = itinerary
	return json.dumps(output)

#print(get_all_data(34.137138, -118.122619,34.149625, -118.150468,0,6*3600))
#pollHereAttractionsBox(LatLng(34.137138, -118.122619),LatLng(34.149625, -118.150468))
#pollHereTravelTime(52.5160,13.3779,52,14)

#shortlist = pollHereAttractions(52.5160,13.3779)
#a = build_itinerary(shortlist[:3], LatLng(52.5160,13.3779), LatLng(52,13), 0, 3600 * 6)







def order_candidates(candidate, start_lat, start_lng):
    '''Returns candidate list of activities in chronological order along with a total score.'''
    ordered_candidate = []
    ordered_candidate_value = 100 # Depends on scoring system
    current = LatLng(start_lat, start_lng)

    while len(candidate) != 0:
            min_distance = 1000000 # Ridiculously large number
            for activity in candidate:
            	actlatlng = LatLng(activity.position.lat, activity.position.lng)
                current_distance = current.dist_to(actlatlng)
                if current_distance < min_distance:
                    min_distance = current_distance
                    best_activity = activity
            ordered_candidate.append(best_activity)
            current_lat = best_activity.position.lat
            current_lng = best_activity.position.lng
            candidate.remove(activity)
            ordered_candidate_value -= current_distance + best_activity.base_score

    return [ordered_candidate, ordered_candidate_value]

def choose_candidate_subsets(activities, num_activities, num_subsets):
    '''Given a list of activities, finds the #(num_subsets) subsets of activities with the highest total scores.'''
    candidates = [] # List of candidate activity lists with associated scores
    subsets = [] # List of all possible subsets with associated scores

    for combination in itertools.combinations(activities, num_activities):
        subset_score = 100 # Depends on scoring system
        for activity in combination:
            subset_score += activity.base_score
        subsets.append([list(combination), subset_score])

    sorted(subsets, key = lambda subset: subset[1])
    candidates = subsets[0:num_subsets] # List of list of activities followed by scores

    return candidates

def make_itinerary_subset(start_lat, start_lng, start_time, end_lat, end_lng, end_time, num_activities, num_subsets):
	itinerary = [] # Final list of activities
	candidates = [] # List of candidate activity lists
	ordered_candidates = [] # list of ordered candidate itineraries followed by total scores
	activities = pollHereAttractions((start_lat + end_lat)/2, (start_lng + end_lng)/2) # Query activities from the midpoint

	sorted(activities, key = lambda activity: activity.base_score) # Sort activities by score
	candidates = choose_candidate_subsets(activities, num_activities, num_subsets)

    # Find best subset by computing traveling time
	for candidate in candidates: # candidate[0] is an array of activities
		ordered_candidates.append(order_candidates(candidate[0], start_lat, start_lng))

	itinerary = max(ordered_candidates, key = operator.itemgetter(1))
	return ordered_candidates







