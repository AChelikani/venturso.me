var platform = new H.service.Platform({
  'app_id': 'N6MJW6UzW079S5ZZwcPl',
  'app_code': 'FOkZLbFrMx77dDpomCs9ZQ'
});

var defaultLayers = platform.createDefaultLayers();
var map;
var ui;

function initialize() {
	var map = new H.Map(
	    document.getElementById('main_map_container'),
	    defaultLayers.normal.map,
	    {
	      zoom: 10,
	      center: { lat: 34.13, lng: -118.12 }
	    });

	var ui = H.ui.UI.createDefault(map, defaultLayers);
}

window.addEventListener('load', initialize, false )