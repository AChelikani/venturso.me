
$(document).ready(function() {

  $("#btnGen").click(function(e) {
    e.preventDefault();
    

    // Grab all the pinned venues we want to include in the journey
    console.log($("form").serialize());
    pinList = "&pinList=["
    $(".pinned").each(function(index) {
      if(index > 0)
        pinList += ",";
      pinList += this.innerHTML;
    });
    pinList += "]"

    // Generate a new itinerary
    $.ajax({
      type : "GET",
      url : "/pathfind",
      data: $("form").serialize() + pinList,
      // data: JSON.stringify(data, null, '\t'),
      // contentType: 'application/json;charset=UTF-8',
      success: function(result) {
          var locations = [];
          var names = [];
          var itinerary = [];
          
          $("#activityList").html("");
          jsonit = JSON.parse(result);
          // console.log(jsonit);
          // Grab all the data for the venue checklist and add the elements
          for(act in jsonit['activityList']) {
            if(jsonit['activityList'][act]['type'] != 'transportation') {
              // console.log(jsonit['activityList'][act]['activity']);

              liElem = $("<li class='list-group-item'>"+jsonit['activityList'][act]['activity']+"</li>");
              if(jsonit[jsonit['activityList'][act]['pinned']]) {
                liElem.addClass("pinned");
              } else if($.inArray(jsonit['activityList'][act]['activity'], jsonit['itinerary']) >= 0) {
                liElem.addClass("selected");
              }
              liElem.on("click", function() {
                // console.log("ay");
                $(this).removeClass("selected");
                if($(this).hasClass("pinned")) {
                  // console.log("Has pinned");
                  $(this).removeClass("pinned");
                } else {
                  $(this).addClass("pinned");
                }
              });
              $("#activityList").append(liElem);
            }
          }

          // Bring in map and data overlay
          var platform = new H.service.Platform({
            'app_id': 'N6MJW6UzW079S5ZZwcPl',
            'app_code': 'FOkZLbFrMx77dDpomCs9ZQ'
          });

          var defaultLayers = platform.createDefaultLayers();
          var map, ui, mapEvents, behavior;

          function calculateRouteFromAtoB(platform, a, b) {
            var router = platform.getRoutingService(),
            routeRequestParams = {
              mode: 'fastest;car',
              representation: 'display',
              routeattributes : 'waypoints,summary,shape,legs',
              maneuverattributes: 'direction,action',
              waypoint0: a, 
              waypoint1: b  
            };

              router.calculateRoute(
                routeRequestParams,
                onSuccess,
                onError
              );
          }

          function onSuccess(result) {
            var route = result.response.route[0];
            addRouteShapeToMap(route);
          }

          function onError(error) {
            alert("Oops!");
          }

          function addRouteShapeToMap(route){
            var strip = new H.geo.Strip(),
              routeShape = route.shape,
              polyline;

            routeShape.forEach(function(point) {
              var parts = point.split(',');
              strip.pushLatLngAlt(parts[0], parts[1]);
            });

            polyline = new H.map.Polyline(strip, {
              style: {
                lineWidth: 4,
                strokeColor: 'rgba(0, 128, 255, 0.7)'
              }
            });
            // Add the polyline to the map
            map.addObject(polyline);
            // And zoom to its bounding rectangle
            map.setViewBounds(polyline.getBounds(), true);
          }

          function initialize() {
            console.log("yo initialize here");
            locations = [];
            names = [];
            itinerary = jsonit['itinerary'];
            for(act in jsonit['activityList']) {
              locations.push(jsonit['activityList'][act]['latitude']);
              locations.push(jsonit['activityList'][act]['longitude']);
              names.push(jsonit['activityList'][act]['activity']);
            }

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

            var point1;
            var point2;
            var counter = 0;

            for(i = 0; i < itinerary.length; i ++) {
              if (itinerary[i].indexOf("Uber") == -1) {
                var temp = itinerary[i];
                var pos = names.indexOf(temp);
                console.log(temp);
                var latlong = [parseFloat(locations[pos*2]), parseFloat(locations[pos*2+1])];
                if (counter == 0) {
                  point1 = String(latlong[0]) + "," + String(latlong[1]);
                  counter ++;
                }
                else {
                  point2 = String(latlong[0]) + "," + String(latlong[1]);
                  calculateRouteFromAtoB(platform, point1, point2);
                  point2 = point1;
                }
                var marker = new H.map.Marker({ lat: latlong[0], lng: latlong[1] });
                map.addObject(marker);
              }
            }

          }

          // window.addEventListener('load', initialize, false );
          initialize();

          }
        });

    $("#main").css("visibility","visible");

  });


});

// I love mixing jquery and javascript in the same file
// function toggle(element) {
//   if (element.className == "list-group-item") {
//     element.className += " pinned";
//   }
//   else {
//     element.className = "list-group-item";
//   }
// }
