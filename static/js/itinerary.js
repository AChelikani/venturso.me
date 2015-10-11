$(document).ready(function() {
	$("#genItinerary").click(function(e) {
		var doc = new jsPDF();
		doc.text(30, 20, "Itinerary");
		doc.save("itinerary.pdf");
	});

});