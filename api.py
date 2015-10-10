import requests
import time
class Transportation:
    TRAVEL_CONST_FACTOR = -1
    def __init__(self, time, start_lat, start_lng, end_lat, end_lng, duration=0):
        self.time = time
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        self.duration = duration
        if duration == 0:
            self.duration = pollHereTravelTime(start_lat, start_lng, end_lat, end_lng)
    
    def value(self):
        return TRAVEL_CONST_FACTOR * self.duration

    def to_json(self):
        return "{'type':'transport', " + \
               "'start_lat': %f, 'start_lng': %f, 'end_lat': %f, 'end_lng': %f}" % (self.start_lat, self.start_lng, self.end_lat, self.end_lng)

class Attraction:
    def __init__(self, name, lat, lng, category, rating, distance=0):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.cat = category
        self.rating = rating
        self.distance = distance
    def duration(self):
        return 7200
    def value(self, prev):
        return -5 + self.rating
    def to_json(self):
        return "{'type':'attraction','lat': %f, 'lng': %f, 'name': '%s', 'cat': '%s'}" % (self.lat, self.lng, self.name, self.cat)
    def __str__(self):
        return "{'name': '%s', 'cat': '%s', 'rating': %f}" % (self.name, self.cat, self.rating)
# Params: latitude, longitude
# Output: [[name1, category1, rating1, [lat1, long1]], etc.]
def pollHere(a, b):
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
        response.append([name, category, rating, location])
    #print time.clock() - start
    return response

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
        response.append(Attraction(name,location[0], location[1], category, rating))
    #print time.clock() - start
    return response

# Params: start lat, start long, end lat, end long
# Output: string of price estimate
def pollUberPrice(a, b, c, d):
    url = "https://api.uber.com/v1/estimates/price?start_latitude=" + str(a) + "&start_longitude=" + str(b) + "&end_latitude=" + str(c) + "&end_longitude=" + str(d) + "&server_token=dVyCwZlJFJ8pUUg3jagY8ETawAkBnygEq3yduosF"
    r = requests.get(url)
    relevant = r.json()
    return relevant["prices"][0]["estimate"]

# Params: start lat, start long, end lat, end long
# Output string of travel time in seconds
# 52.5160,13.3779,52.5206,13.3862
def pollHereTravelTime(a, b, c, d):
    #start = time.clock()
    a,b,c,d = map(str, [a,b,c,d])
    url = "https://route.cit.api.here.com/routing/7.2/calculateroute.json?waypoint0=" + a + "%2C" + b + "&waypoint1=" + c + "%2C" + d + "&mode=fastest%3Bcar%3Btraffic%3Aenabled&app_id=N6MJW6UzW079S5ZZwcPl&app_code=FOkZLbFrMx77dDpomCs9ZQ&tf&departure=now"
    r = requests.get(url)
    relevant = r.json()
    #print time.clock() - start
    return relevant["response"]["route"][0]["leg"][0]["travelTime"]


# print pollHereTravelTime(1, 1, 1, 1)
# print pollUber(34.139011, -118.124514, 34.130647, -118.147108)
# print poll(34.139011, -118.124514)        

    


