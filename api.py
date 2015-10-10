import requests


# Params: latitude, longitude
# Output: [[name1, category1, rating1, [lat1, long1]], etc.]
def pollHere(a, b):
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
    return response

# Params: start lat, start long, end lat, end long
# Output: string of price estimate
def pollUberPrice(a, b, c, d):
    url = "https://api.uber.com/v1/estimates/price?start_latitude=" + str(a) + "&start_longitude=" + str(b) + "&end_latitude=" + str(c) + "&end_longitude=" + str(d) + "&server_token=dVyCwZlJFJ8pUUg3jagY8ETawAkBnygEq3yduosF"
    r = requests.get(url)
    relevant = r.json()
    return relevant["prices"][0]["estimate"]

# Params: start lat, start long, end lat, end long
# Output string of travel time in minutes
def pollHereTravelTime(a, b, c, d):
    url = "https://route.cit.api.here.com/routing/7.2/calculateroute.json?waypoint0=52.5160%2C13.3779&waypoint1=52.5206%2C13.3862&mode=fastest%3Bcar%3Btraffic%3Aenabled&app_id=N6MJW6UzW079S5ZZwcPl&app_code=FOkZLbFrMx77dDpomCs9ZQ&tf&departure=now"
    r = requests.get(url)
    relevant = r.json()
    return relevant["response"]["route"][0]["leg"][0]["travelTime"]

# print pollHereTravelTime(1, 1, 1, 1)
# print pollUber(34.139011, -118.124514, 34.130647, -118.147108)
# print poll(34.139011, -118.124514)        

    


