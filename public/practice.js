let menu = {
  1 : ["Chair", "Table", "Sofa", "Desk","Merlot", "Shiraz", "Cabernet", "Chardonnay","Saturn", "Venus", "Jupiter", "Mercury","France", "England", "Germany", "Spain"],
  2 : ["Pecan", "Walnut", "Almond", "Pistachio","Sapphire", "Topaz", "Pearl", "Emerald","Blimp", "Helicopter", "Airplane", "Balloon","Minotaur", "Sasquatch","Ogopogo", "Bigfoot"],
  3 : ["Sunflower", "Canola", "Olive", "Sesame","Football", "Baseball", "Soccer", "Basketball","China", "Japan", "India", "Vietnam","Banana", "Apple", "Pear", "Mango"]
}
let menu_order = [2,3];
let word_order = [11,5];
let trial_number = 0;
let word;
let id = "#menu2-section3-item4";
let id2 = "#menu3-section2-item2"

$(document).ready(function() {
  $("#experiment").hide();
  $("#prompt").hide();
  $(".introduction1").show();
  $(".introduction2").hide();
  $(".introduction3").hide();
  $(".done").hide();
});

function init(){
  for (let i = 0; i < 16; i++){
    let section = Math.ceil(i/4);
    let item = i%4+1;
    let id = "#menu1-section" + section + "-item" + item;
    $(id).text(menu[1][i]);
    if (trial_number === 1){
      $(id).addClass("fading");
    }
  }
  for (let i = 0; i < 16; i++){
    let section = Math.ceil(i/4);
    let item = i%4+1;
    let id = "#menu2-section" + section + "-item" + item;
    $(id).text(menu[2][i]);
    if (trial_number === 1){
      $(id).addClass("fading");
    }
  }
  for (let i = 0; i < 16; i++){
    let section = Math.ceil(i/4);
    let item = i%4+1;
    let id = "#menu3-section" + section + "-item" + item;
    $(id).text(menu[3][i]);
    if (trial_number === 1){
      $(id).addClass("fading");
    }
  }
  if (trial_number === 1){
    $("#menu3-section2-item2").removeClass("fading");
    $("#menu3-section1-item3").removeClass("fading");
    $("#menu3-section4-item2").removeClass("fading");
  }
  word = menu[menu_order[trial_number]][word_order[trial_number]];
  $("#prompt").text("Menu " + menu_order[trial_number] + " > " + word);
}

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
  init();
  $("#prompt").show();
});

$(id).on("click", function(){
  trial_number = trial_number + 1;
  init();
});

$(id2).on("click", function(){
  $(".done").show();
  $("#experiment").hide();
  $("#prompt").hide();
});
