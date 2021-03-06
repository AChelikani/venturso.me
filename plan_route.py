import algorithms2
from algorithms2 import Transportation
from algorithms2 import Attraction
import json
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

def add_transportation(array, current_time, start_lat, start_lng, end_lat, end_lng, travel_time=0):
	t = Transportation(current_time, start_lat, start_lng, end_lat, end_lng, travel_time)
	array.append(t)
	return current_time + t.duration

def time_to_end(start_lat, start_lng, end_lat, end_lng):
	return algorithms2.pollHereTravelTime(start_lat, start_lng, end_lat, end_lng)

def jsonify(itinerary):
	return "[" + ",".join(map(lambda x: x.to_json(), itinerary)) + "]"

def make_itinerary(start_lat, start_lng, start_time, end_lat, end_lng, end_time):
	itinerary = []

	current_time = start_time
	lat, lng = start_lat, start_lng

	activities = algorithms2.pollHereAttractions(lat, lng)

	distance_scaling = algorithms2.pollHereTravelTime(start_lat, start_lng, end_lat, end_lng)

	# Main loop
	while (end_time - current_time) > time_to_end(lat, lng, end_lat, end_lng) and len(activities) > 0:
		best_score = -100 # set to lowest score
		best_activity = "null"
		travel_time = algorithms2.pollHereTravelTime(lat, lng, end_lat, end_lng)
		for activity in activities:
			#print (activity.name, travel_time, best_activity)
			if end_time - current_time > travel_time + activity.duration():
				current_score = activity.value(itinerary)
				if current_score > best_score:
					best_score = current_score
					best_activity = activity

		if best_activity == "null": break
		current_time = add_transportation(itinerary, current_time, lat, lng, best_activity.lat, best_activity.lng)
		itinerary.append(best_activity)
		#print itinerary
		activities.remove(best_activity)
		current_time += best_activity.duration()
		lat,lng = best_activity.lat, best_activity.lng

	add_transportation(itinerary, current_time, lat, lng, end_lat, end_lng)

	return itinerary

def get_itinerary_as_json(start_lat, start_lng, start_time, end_lat, end_lng, end_time):
	return jsonify(make_itinerary(start_lat, starprintt_lng, start_time, end_lat, end_lng, end_time))
		
		#update(current_location, current_time)

# -----------

def order_candidates(candidate, start_lat, start_lng):
    '''Returns candidate list of activities in chronological order along with a total score.'''
    ordered_candidate = []
    ordered_candidate_value = 100 # Depends on scoring system
    current_lat = start_lat
    current_lng = start_lng

    while len(candidate) != 0:
            min_distance = 1000000 # Ridiculously large number
            for activity in candidate:
                current_distance = distance(current_lat, current_lng, activity.lat, activity.lng)
                if current_distance < min_distance:
                    min_distance = current_distance
                    best_activity = activity
            ordered_candidate.append(best_activity)
            current_lat = best_activity.lat
            current_lng = best_activity.lng
            del candidate[activity]
            ordered_candidate_value -= current_distance + best_activity.value()

    return (candidate, ordered_candidate_value)

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
    candidates = subsets[0:num_subsets]

def make_itinerary_subset(start_lat, start_lng, start_time, end_lat, end_lng, end_time, num_activities, num_subsets):
	itinerary = []
	candidates = []
	ordered_candidates = {} # key: ordered candidate itinerary; value: total modified score
	activities = algorithms2.pollHereAttractions((start_lat + end_lat)/2, (start_lng + end_lng)/2) # Query activities from the midpoint

	sorted(activities, key = lambda activity: activity.base_score) # Sort activities by score
	candidates = choose_candidate_subsets(activities, num_activities, num_subsets)

    # Find best subset by computing traveling time
	for candidate in candidates: # candidate is an array of activities
		dict_tuple = order_candidates(candidate)
		ordered_candidates[dict_tuple[0]] = dict_tuple[1]

	itinerary = max(ordered_candidates.iteritems(), key=operator.itemgetter(1))[0]
	return itinerary







