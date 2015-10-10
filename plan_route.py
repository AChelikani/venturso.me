import api
from api import Transportation
from api import Attraction
import json

def add_transportation(array, current_time, start_lat, start_lng, end_lat, end_lng, travel_time=0):
	t = Transportation(current_time, start_lat, start_lng, end_lat, end_lng, travel_time)
	array.append(t)
	return current_time + t.duration

def time_to_end(start_lat, start_lng, end_lat, end_lng):
	return api.pollHereTravelTime(start_lat, start_lng, end_lat, end_lng)

def jsonify(itinerary):
	return "[" + ",".join(map(lambda x: x.to_json(), itinerary)) + "]"

def make_itinerary(start_lat, start_lng, start_time, end_lat, end_lng, end_time):
	itinerary = []

	current_time = start_time
	lat, lng = start_lat, start_lng

	activities = api.pollHereAttractions(lat, lng)
	#print activities
	# Main loop
	while (end_time - current_time) > time_to_end(lat, lng, end_lat, end_lng) and len(activities) > 0:
		best_score = -100 # set to lowest score
		best_activity = "null"

		for activity in activities:
			travel_time = api.pollHereTravelTime(lat, lng, activity.lat, activity.lng)
			#print (activity.name, travel_time, best_activity)
			if end_time - current_time > travel_time + activity.duration():
				current_score = activity.value(itinerary)
				if current_score > best_score:
					best_score = current_score
					best_activity = activity

		if best_activity == "null": break
		current_time = add_transportation(itinerary, current_time, lat, lng, best_activity.lat, best_activity.lng)
		itinerary.append(best_activity)
		print itinerary
		activities.remove(best_activity)
		current_time += best_activity.duration()
		lat,lng = best_activity.lat, best_activity.lng

	add_transportation(itinerary, current_time, lat, lng, end_lat, end_lng)

	return itinerary
		
		#update(current_location, current_time)