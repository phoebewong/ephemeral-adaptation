$(document).ready(function() {
  $("#experiment").hide();
  $("#prompt").hide();
  $(".introduction1").show();
  $(".introduction2").hide();
  $(".introduction3").hide();
  $(".done").hide();
});

$("#introduction1-button").on("click", function(){
  $(".introduction1").hide();
  $(".introduction2").show();
});

$("#introduction2-button").on("click", function(){
  $(".introduction2").hide();
  $(".introduction3").show();
});

$("#introduction3-button").on("click", function(){
  $(".introduction3").hide();
  $("#experiment").show();
  $("#prompt").text("HENLO");
  $("#prompt").show();
});

$(".navbar").on("click", function(){
  $(".done").show();
  $("#experiment").hide();
  $("#prompt").hide();
});
