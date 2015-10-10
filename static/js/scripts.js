
$(document).ready(function() {

  $("#btnGen").click(function(e) {
    e.preventDefault();
    console.log($("form").serialize()+"&pinList=[]");
    
    $.ajax({
      type : "GET",
      url : "/pathfind",
      data: $("form").serialize(),
      // data: JSON.stringify(data, null, '\t'),
      // contentType: 'application/json;charset=UTF-8',
      success: function(result) {
          $("#activityList").html("");
          jsonit = JSON.parse(result);
          // console.log(jsonit);
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
                if($(this).hasClass("pinned")) {
                  // console.log("Has pinned");
                  $(this).removeClass("pinned");
                  $(this).removeClass("selected");
                } else {
                  $(this).addClass("pinned");
                }
              });
              $("#activityList").append(liElem);

            }
          }
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
