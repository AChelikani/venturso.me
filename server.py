from flask import Flask
from flask import render_template
from flask import request
import json
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

# Called to gen the map. Dump all the algorithm junk here. Should accept from
# address, to address, from time, to time, and optional optimization parameters
#
# Example to use:
# http://localhost:5000/pathfind?from=Berkeley&to=Caltech&fromtime=Oct10&totime=Oct12
@app.route('/pathfind', methods=['GET'])
def path_find():
	print request.args['from']
	print request.args['to']
	print request.args['fromtime']
	print request.args['totime']
	print request.args['pinList']
	

	jsonJunk = {'activityList': [{'activity': 'Dodger Stadium','latitude': '34.072958','longitude': '-118.240648','type': 'attraction', 'pinned':'false'},{'activity': 'Huntington Beach','latitude': '33.661622','longitude': '-118.008125','type': 'attraction', 'pinned':'false'},{'activity': 'Chipotle','latitude': '34.141782','longitude': '-118.132289','type': 'food', 'pinned':'false'},{'activity': 'Uber1','latitude': '0','longitude': '0','type': 'transportation', 'pinned':'false'},{'activity': 'Uber2','latitude': '0','longitude': '0','type': 'transportation', 'pinned':'false'},{'activity': 'Griffith Observatory','latitude': '34.118487','longitude': '-118.300372','type': 'attraction', 'pinned':'false'}],'itinerary': ['Griffith Observatory', 'Uber1', 'Chipotle', 'Uber2', 'Dodger Stadium']}
	print json.dumps(jsonJunk)
	return json.dumps(jsonJunk)


if __name__ == '__main__':
    # app.run()
	app.run(debug=True)

