from flask import Flask
from flask import render_template
from flask import request
import json
import algorithms2
import os
app = Flask(__name__)

# Splash page!
# To run, type into browser: localhost:5000
@app.route('/')
def splash():
	return render_template('splash.html')

# Called after splash page. Should only display from, to junk and button to
# gen the map
@app.route('/creation')
def create_tour():
	return render_template('creation.html')

@app.route('/map')
def map_page():
	return render_template('map.html')


def get_time(string):
	hour = minute = 0
	if "PM" in string: hour += 12
	string = string.replace("PM", "")
	string = string.replace("AM", "")
	s_hour, s_min = string.split(":")
	hour += int(s_hour)
	if hour == 24: 
		hour = 12
	minute += int(s_min)
	return 3600 * hour + 60 * minute
# Called to gen the map. Dump all the algorithm junk here. Should accept from
# address, to address, from time, to time, and optional optimization parameters
#
@app.route('/pathfind', methods=['GET'])
def path_find():
	#print request.args['from']
	#print request.args['to']
	#print request.args['fromtime']
	#print request.args['totime']
	#print request.args['pinList']
	#print [request.args['start_lat'], request.args['start_lng'], \
		#request.args['end_lat'], request.args['end_lng']]
	a,b,c,d = map(float, [request.args['start_lat'], request.args['start_lng'], \
		request.args['end_lat'], request.args['end_lng']])
	try:
		start_time = get_time(str(request.args['fromtime']))
	except:
		start_time = 0
	try:
		end_time = get_time(str(request.args['totime']))
	except:
		end_time = 6 * 3600
	print (str(request.args['fromtime']), str(request.args['totime']))
	print (start_time, end_time)
	return algorithms2.get_all_data(a, b, c, d, start_time, end_time, request.args['pinList'], request.args['rejList'])
	#return algorithms2.get_all_data(34.137138, -118.122619,34.149625, -118.150468,0,6*3600)
	jsonJunk = {'activityList': [{'activity': 'Dodger Stadium','latitude': '34.072958','longitude': '-118.240648','type': 'attraction', 'pinned':'false'},{'activity': 'Huntington Beach','latitude': '33.661622','longitude': '-118.008125','type': 'attraction', 'pinned':'false'},{'activity': 'Chipotle','latitude': '34.141782','longitude': '-118.132289','type': 'food', 'pinned':'false'},{'activity': 'Uber1','latitude': '0','longitude': '0','type': 'transportation', 'pinned':'false'},{'activity': 'Uber2','latitude': '0','longitude': '0','type': 'transportation', 'pinned':'false'},{'activity': 'Griffith Observatory','latitude': '34.118487','longitude': '-118.300372','type': 'attraction', 'pinned':'false'}],'itinerary': ['Griffith Observatory', 'Uber1', 'Chipotle', 'Uber2', 'Dodger Stadium']}
	jsonJunk = {'activityList': [{
		"type": "transportation",
		"start": {
			"lat": 52.516,
			"lng": 13.3779
		},
		"end": {
			"lat": 52.523441,
			"lng": 13.38407
		},
		"name":"transport1",
		"cat":"Uber"
	},
	{
		"type": "attraction",
		"position": {
			"lat": 52.523441,
			"lng": 13.38407
		},
		"name": "Sammlung Boros",
		"cat": "Sights & Museums"
	},
	{
		"type": "transportation",
		"start": {
			"lat": 52.523441,
			"lng": 13.38407
		},
		"end": {
			"lat": 52.519371,
			"lng": 13.39693
		},
		"name":"transport2",
		"cat":"Uber"

	},
	{
		"type": "attraction",
		"position": {
			"lat": 52.519371,
			"lng": 13.39693
		},
		"name": "Contemporary Fine Arts",
		"cat": "Sights & Museums"
	},
	{
		"type": "transportation",
		"start": {
			"lat": 52.519371,
			"lng": 13.39693
		},
		"end": {
			"lat": 52.51471,
			"lng": 13.3905
		},
		"name":"transport3",
		"cat":"Uber"
	},
	{
		"type": "attraction",
		"position": {
			"lat": 52.51471,
			"lng": 13.3905
		},
		"name": "Ritter Sport Bunte Schokowelt",
		"cat": "Kiosk/24-7/Convenience Store"
	},
	{
		"type": "transportation",
		"start": {
			"lat": 52.51471,
			"lng": 13.3905
		},
		"end": {
			"lat": 52.5094,
			"lng": 13.37366
		},
		"name":"transport4",
		"cat":"Uber"
	},
	{
		"type": "attraction",
		"position": {
			"lat": 52.5094,
			"lng": 13.37366
		},
		"name": "Arsenal",
		"cat": "Cinema"
	},
	{
		"type": "transportation",
		"start": {
			"lat": 52.5094,
			"lng": 13.37366
		},
		"end": {
			"lat": 52.52758,
			"lng": 13.40302
		},
		"name":"transport5",
		"cat":"Uber"
	},
	{
		"type": "attraction",
		"position": {
			"lat": 52.52758,
			"lng": 13.40302
		},
		"name": "b-flat - Accoustic Musik and Jazz Club",
		"cat": "Theatre, Music & Culture"
	},
	{
		"type": "transportation",
		"start": {
			"lat": 52.52758,
			"lng": 13.40302
		},
		"end": {
			"lat": 52,
			"lng": 14
		},
		"name":"transport6",
		"cat":"Uber"
	 }
	],'itinerary': ['Arsenal', 'transport1', 'b-flat - Accoustic Musik and Jazz Club', 'transport2', 'Ritter Sport Bunte Schokowelt']}

	print json.dumps(jsonJunk)
	return json.dumps(jsonJunk)


if __name__ == '__main__':
	# app.run()
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)

