let menu = {
  1 : ["Chair", "Table", "Sofa", "Desk","Merlot", "Shiraz", "Cabernet", "Chardonnay","Saturn", "Venus", "Jupiter", "Mercury","France", "England", "Germany", "Spain"],
  2 : ["Pecan", "Walnut", "Almond", "Pistachio","Fall", "Summer", "Spring", "Winter","Blimp", "Helicopter", "Airplane", "Balloon","Red", "Blue","Yellow", "Green"],
  3 : ["Shirt", "Pants", "Short", "Skirt","Football", "Baseball", "Soccer", "Basketball","China", "Japan", "India", "Vietnam","Banana", "Apple", "Pear", "Mango"]
}
let menu_order = [2,3,1,2,1,2,1,3];
let word_order = [11,5,4,1,6,5,3,7];
let trial_number = 0;
let word;
let ids = {
  0: "#menu2-section3-item4",
  1: "#menu3-section2-item2",
  2: "#menu1-section2-item1",
  3: "#menu2-section1-item2",
  4: "#menu1-section2-item3",
  5: "#menu2-section2-item2",
  6: "#menu1-section1-item4",
  7: "#menu3-section2-item4"
};
let correct_id = ids[trial_number];
let condition_order = [];

$(document).ready(function() {
  $("#experiment").hide();
  $("#prompt").hide();
  $(".introduction1").show();
  $(".introduction2").hide();
  $(".introduction3").hide();
  $(".middle").hide();
  $(".done").hide();
});

function update(){
  correct_id = ids[trial_number];
  $(correct_id).prop("onclick", null).off("click");

  $(correct_id).on("click", function(){
    if (trial_number === 7){
      $(".done").show();
      $("#experiment").hide();
      $("#prompt").hide();
    }
    if (trial_number === 3){
      $(".middle").show();
      $("#experiment").hide();
      $("#prompt").hide();
      trial_number = trial_number + 1;
      update();
    }
    else {
      trial_number = trial_number + 1;
      update();
    }
  });

  for (let i = 0; i < 16; i++){
    let section = Math.floor(i/4)+1;
    let item = i%4+1;
    let id = "#menu1-section" + section + "-item" + item;
    $(id).text(menu[1][i]);
    if (trial_number < 4){
      $(id).addClass("fading");
    }
    else {
      $(id).removeClass("fading");
    }
  }
  for (let i = 0; i < 16; i++){
    let section = Math.floor(i/4)+1;
    let item = i%4+1;
    let id = "#menu2-section" + section + "-item" + item;
    $(id).text(menu[2][i]);
    if (trial_number < 4){
      $(id).addClass("fading");
    }
    else {
      $(id).removeClass("fading");
    }
  }
  for (let i = 0; i < 16; i++){
    let section = Math.floor(i/4)+1;
    let item = i%4+1;
    let id = "#menu3-section" + section + "-item" + item;
    $(id).text(menu[3][i]);
    if (trial_number < 4){
      $(id).addClass("fading");
    }
    else {
      $(id).removeClass("fading");
    }
  }
  if (trial_number < 4){
    let menu_var = menu_order[trial_number]
    $("#menu" + menu_var + "-section" + menu_var + "-item4").removeClass("fading");
    $("#menu" + menu_var + "-section1-item2").removeClass("fading");
    $("#menu" + menu_var + "-section2-item2").removeClass("fading");
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
  update();
  $("#prompt").show();
});

$("#middle-button").on("click", function(){
  $(".middle").hide();
  $("#experiment").show();
  $("#prompt").show();
});
