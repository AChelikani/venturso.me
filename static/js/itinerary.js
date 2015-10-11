$(document).ready(function() {
	$("#genItinerary").click(function(e) {
		var currentLine = 20;
		var cBuffer = 40;
		var doc = new jsPDF();
		doc.text(50, currentLine, "Itinerary");
		currentLine += 20;

		var start = document.getElementById("start").value;
		var end = document.getElementById("end").value;
		var from = document.getElementById("from").value;
		var to = document.getElementById("to").value;

		doc.text(20, currentLine, from + "     |     " + start);
		currentLine += 10;
		doc.text(20, currentLine, to = "     |     " + end);
		currentLine += 10;


		doc.save("itinerary.pdf");
	});

});