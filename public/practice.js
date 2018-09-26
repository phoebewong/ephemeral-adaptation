$(document).ready(function() {
  $("#experiment").hide();
  $(".introduction").show();
  $("#prompt").hide();
  $("#experiment-button").hide();
});

$("#introduction-button").on("click", function(){
  // $("#experiment").show();
  // $(".introduction").hide();
  // $("#prompt").show();
  $("#introduction-button").hide();
  $("#experiment-button").show();
});
