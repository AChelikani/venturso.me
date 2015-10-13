// Construct PDF give itinerary
$(document).ready(function() {
	$("#genItinerary").click(function(e) {
		var currentLine = 20;
		var cBuffer = 40;
		var doc = new jsPDF();
		doc.setFontSize(20)
		doc.text(20, currentLine, "Your Tourism Plan:");
		doc.setFontSize(16)
		currentLine += 10;

		// Get form values
		var start = document.getElementById("start").value;
		var end = document.getElementById("end").value;
		var from = document.getElementById("from").value;
		var to = document.getElementById("to").value;

		// Print form values to PDF
		doc.text(20, currentLine, "Start from:  " + from + "     |     " + start);
		currentLine += 10;
		doc.text(20, currentLine, "Finish at:   " + to + "     |     " + end);
		currentLine += 20;

		// Print itinerary by looking through JSON adding items to PDF
		doc.setFontSize(20)
		doc.text(20, currentLine, "Itinerary:");
		doc.setFontSize(16)
		currentLine += 10;
		if (jsonit) {
			var start_time = jsonit['init_time']
            console.log(start_time)
            for (i in jsonit['itinerary']) {
              console.log(jsonit['itinerary'][i])
              var text =jsonit['itinerary'][i]["name"]
              if (text.indexOf('transport') < 0) {
              	doc.text(20, currentLine, jsonit['itinerary'][i]["name"] + "     |     " + seconds_to_time(start_time) + "     |     " + seconds_to_time(parseInt(jsonit['itinerary'][i]["end_time"])));
				currentLine += 10;	
              }
              start_time = parseInt(jsonit['itinerary'][i]["end_time"])
            }
		}
		doc.save("itinerary.pdf");
	});

});