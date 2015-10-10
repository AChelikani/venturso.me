from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

# Splash page!
@app.route('/')
def splash():
    return render_template('splash.html')

# Called after splash page. Should only display from, to junk and button to
# gen the map
@app.route('/creation')
def create_tour():
    return render_template('creation.html')

# Called to gen the map. Dump all the algorithm junk here. Should accept from
# address, to address, from time, to time, and optional optimization parameters
@app.route('/pathfind', methods=['GET'])
def path_find():
	print request.args['from']
	print request.args['to']
	print request.args['fromtime']
	print request.args['totime']
	return "Hello World"

if __name__ == '__main__':
    app.run()



