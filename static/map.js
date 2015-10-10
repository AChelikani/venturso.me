var platform = new H.service.Platform({
  'app_id': 'N6MJW6UzW079S5ZZwcPl',
  'app_code': 'FOkZLbFrMx77dDpomCs9ZQ'
});

var defaultLayers = platform.createDefaultLayers();
var map;
var ui;
var mapEvents;
var behavior;

function initialize() {
	map = new H.Map(
	    document.getElementById('map-canvas'),
	    defaultLayers.normal.map,
	    {
	      zoom: 10,
	      center: { lat: 34.13, lng: -118.12 }
	    });

	ui = H.ui.UI.createDefault(map, defaultLayers);

	mapEvents = new H.mapevents.MapEvents(map);
	behavior = new H.mapevents.Behavior(mapEvents);
}

window.addEventListener('load', initialize, false )