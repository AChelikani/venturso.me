var start_lat //= 34.137138
var start_lng //= -118.122619
var end_lat //= 34.149625
var end_lng //= -118.150468
var map;
function name_to_id(my_name) {
  return (my_name.split(/[^A-Za-z]/)).join("-")
}


function seconds_to_time(seconds) {
    hours = Math.floor(seconds / 3600) % 24
    minutes = Math.floor((seconds % 3600)/60)
    return minutes < 10? hours+":0"+minutes : hours+":"+minutes
}

$(document).ready(function() {

  $("#btnGen").click(function(e) {
    e.preventDefault();
    $("#main").css("visibility","hidden");
    // Bring in map and data overlay
    var platform = new H.service.Platform({
      'app_id': 'N6MJW6UzW079S5ZZwcPl',
      'app_code': 'FOkZLbFrMx77dDpomCs9ZQ'
    });

    var geocoder = platform.getGeocodingService()
    geocodingParameters = {
      searchText: document.getElementById("from").value,
      jsonattributes : 1
    };
    geocoder.geocode(geocodingParameters, function(result) {
      start_lat = result.response.view[0].result[0].location.displayPosition.latitude
      start_lng = result.response.view[0].result[0].location.displayPosition.longitude 

      geocodingParameters = {
        searchText: document.getElementById("to").value,
        jsonattributes : 1
      };
      geocoder.geocode(geocodingParameters, function(result) {
        end_lat = result.response.view[0].result[0].location.displayPosition.latitude
        end_lng = result.response.view[0].result[0].location.displayPosition.longitude 

        generate_everything(start_lat, start_lng, end_lat, end_lng)
      }, function(error) {console.log(error)});
    }, function(error) {console.log(error)});
     

    // Grab all the pinned venues we want to include in the journey
    console.log($("form").serialize());
    pinList = "&pinList=["
    $(".pinned").each(function(index) {
      if(index > 0)
        pinList += ",";
      pinList += this.innerHTML;
    });
    pinList += "]"

    // Grab all the rejected venues we want to exclude from the journey
    rejList = "&rejList=["
    $(".rejected").each(function(index) {
      if(index > 0)
        rejList += ",";
      rejList += this.innerHTML;
    });
    rejList += "]"


    // Generate a new itinerary\
    function generate_everything(start_lat, start_lng, end_lat, end_lng) {
      $("#loading-wrapper").removeClass("hidden")
      $.ajax({
        type : "GET",
        url : "/pathfind",
        data: $("form").serialize() + pinList + rejList + "&start_lat="+start_lat+"&start_lng="+start_lng+"&end_lat="+end_lat+"&end_lng="+end_lng,
        // data: JSON.stringify(data, null, '\t'),
        // contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          if (map) map.removeObjects(map.getObjects());
          document.getElementById('itinerary').innerHTML = '<tbody><tr id="header-row"><th>Location</th><th>Arrival Time</th><th>Departure Time</th></tr></tbody>'
            $("#activityList").html(""); // Clear previous itinerary
            jsonit = JSON.parse(result);
            // console.log(jsonit);
            // Grab all the data for the venue checklist and add the elements
            
            
            for(act in jsonit['activityList']) {
              if(jsonit['activityList'][act]['type'] != 'transportation') {
                // console.log(jsonit['activityList'][act]['name']);
                console.log(jsonit['itinerary']);
                // console.log(jsonit['itinerary'].indexOf(jsonit['activityList'][act]['name']));
                
                // Contains function to check if something is in the itinerary
                function contains(arr, obj) {
                    for (i in arr) {
                        if (arr[i]['name'] === obj) {
                            return true;
                        }
                    }
                    return false;
                }
                function add_to_table(idstr) {
                  /*for (i in jsonit['itinerary']) {
                    if (name_to_id(jsonit['itinerary'][i]["name"]) == idstr) {
                      $("#itinerary tbody").append("<tr id='" + idstr+"TABLE" + "'>" +
                        "<td>" + jsonit['itinerary'][i]["name"] + "</td>" +
                        "<td>"+ jsonit['itinerary'][i]["end_time"] + "</td>" +
                        "<td>"+ jsonit['itinerary'][i]["end_time"] + "</td>");
                    }
                  }*/ 
                }

                // Setting up the status of the venues when creating the list

                liElem = $("<li class='list-group-item' id='"+name_to_id(jsonit['activityList'][act]['name'])+"'>"+jsonit['activityList'][act]['name']+"</li>");
                if(pinList.indexOf(jsonit['activityList'][act]['name']) >= 0) {
                  // It's pinned
                  console.log("PINNED");
                  liElem.addClass("pinned");
                  add_to_table(name_to_id(jsonit['activityList'][act]['name']));
                } else if(contains(jsonit['itinerary'], jsonit['activityList'][act]['name'])) {
                  // It's selected
                  console.log("SELECTED");
                  liElem.addClass("selected");
                  add_to_table(name_to_id(jsonit['activityList'][act]['name']));
                } else if(rejList.indexOf(jsonit['activityList'][act]['name']) >= 0) {
                  // It's rejected
                  console.log("REJECTED");
                  liElem.addClass("rejected");
                } //else { /* It's not selected */ }
                
                // Add the event listener to toggle through states
                liElem.on("click", function() {
                  var idstr = $(this).attr('id');
                  if($(this).hasClass("selected")) {
                    $(this).removeClass("selected");
                    $(this).addClass("pinned");
                  } else if($(this).hasClass("pinned")) {
                    // It's pinned. Cycle to rejected.
                    console.log("tr #" + idstr+"TABLE")
                    $("tbody #" + idstr+"TABLE").remove();
                    $(this).removeClass("pinned");
                    $(this).addClass("rejected");
                  } else if($(this).hasClass("rejected")) {
                    $(this).removeClass("rejected");
                  } else {
                    $(this).addClass("pinned");
                    add_to_table(idstr);
                  }
                });
                $("#activityList").append(liElem);
              }
            }
            var start_time = jsonit['init_time']
            console.log(start_time)
            for (i in jsonit['itinerary']) {
              console.log(jsonit['itinerary'][i])
              var text =jsonit['itinerary'][i]["name"]
              if (text.indexOf('transport') < 0) {

                idstr = name_to_id(jsonit['itinerary'][i]["name"])
                $("#itinerary tbody").append("<tr id='" + idstr+"TABLE" + "'>" +
                  "<td>" + text + "</td>" +
                  "<td>"+ seconds_to_time(start_time) + "</td>" +
                  "<td>"+ seconds_to_time(parseInt(jsonit['itinerary'][i]["end_time"])) + "</td>");
              }
              start_time = parseInt(jsonit['itinerary'][i]["end_time"])
            }

            var defaultLayers = platform.createDefaultLayers();
            var ui, mapEvents, behavior;

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
              console.log(error);
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
                if(jsonit['activityList'][act]['position'] != undefined){
                  locations.push(jsonit['activityList'][act]['position']['lat']);
                  locations.push(jsonit['activityList'][act]['position']['lng']);
                  names.push(jsonit['activityList'][act]['name']);
                }
              }
              console.log(locations);
              console.log(names);

              if (map == null) {
                map = new H.Map(
                    document.getElementById('map-canvas'),
                    defaultLayers.normal.map,
                    {
                      zoom: 10,
                      center: { lat: (start_lat + end_lat)/2, lng: (start_lng + end_lng)/2 }
                    });

                ui = H.ui.UI.createDefault(map, defaultLayers);

                mapEvents = new H.mapevents.MapEvents(map);
                behavior = new H.mapevents.Behavior(mapEvents);
              }

              var point1;
              var point2;
              var counter = 0;

              for(i = 0; i < itinerary.length; i ++) {
                if (itinerary[i]["name"].indexOf("transport") == -1) {
                  var temp = itinerary[i]["name"];
                  var pos = names.indexOf(temp);
                  console.log(temp);
                  var latlong = [parseFloat(locations[pos*2]), parseFloat(locations[pos*2+1])];
                  if (counter == 0) {
                    point1 = String(latlong[0]) + "," + String(latlong[1]);
                    var marker = new H.map.Marker({ lat: start_lat, lng: start_lng}, 
                                                  {icon: new H.map.Icon("static/marker.png")});
                    map.addObject(marker);
                    calculateRouteFromAtoB(platform, start_lat+","+start_lng,point1);
                    counter ++;
                  }
                  else {
                    point2 = String(latlong[0]) + "," + String(latlong[1]);
                    calculateRouteFromAtoB(platform, point1, point2);
                    point2 = point1;
                  }

                  var marker = new H.map.Marker({ lat: latlong[0], lng: latlong[1] });
                  marker.setData(name_to_id(itinerary[i]["name"]))
                  marker.addEventListener('pointerenter', function(e) {
                    var tr = document.getElementById(this.getData()+"TABLE")
                    if (tr) { tr.style = "background-color: #f1f1f1"}
                  });
                  marker.addEventListener('pointerleave', function(e) {
                    var tr = document.getElementById(this.getData()+"TABLE")
                    if (tr) { tr.style = "" }
                  });
                  map.addObject(marker);
                }
              }
              calculateRouteFromAtoB(platform,point1, end_lat+","+end_lng);   
              var marker = new H.map.Marker({ lat: end_lat, lng: end_lng}, 
                                            {icon: new H.map.Icon("static/marker.png")});
              map.addObject(marker); 

              $("#loading-wrapper").addClass("hidden")  

              $("#main").css("visibility","visible");   
            }

            // window.addEventListener('load', initialize, false );
            initialize();

            }


          });

      }

    

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
