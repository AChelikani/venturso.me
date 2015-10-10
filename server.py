from flask import Flask
from flask import render_template
from flask import request
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
	
	

	return "{'activityList': [{activity: 'Eiffel Tower',latitude: lat,longitude: long,type: 'attraction'},{activity: 'Le Louvre',latitude: lat,longitude: long,type: 'attraction'},{activity: 'Best Paris Baguettes',latitude: lat,longitude: long,type: 'food'},{activity: 'Uber1',latitude: lat,longitude: long,type: 'transportation'},{activity: 'Uber2',latitude: lat,longitude: long,type: 'transportation'}],'itinerary': ['Eiffel Tower', 'Uber1', 'Best Paris Baguettes', 'Uber2', 'Le Louvre']}"


if __name__ == '__main__':
    # app.run()
	app.run(debug=True)

