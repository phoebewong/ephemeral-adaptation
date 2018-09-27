let exp;
let experiment_number;
let technique; // Either control or ephemeral
let condition_order;
let condition = 0;
let block_number = 0;
let trial_number = 0;
let answer;
let correct_id;
let correct_word;
let num_trials;
let abrupt_onset_words = [];
let end = 0;
let start = 0;
let stop = 0;
let correct_menu;
let started = 0;

let data = {
  "condition_sequence": "",
  "experiment_number": "",
  "number_trials": "",
  "trials": []
};

let qualitative_information = {
}

function init(){
  $.get({
      url: "/data",
      success: function (data) {
        console.log(data);
        let len = data.length;
        experiment_number = Math.floor(Math.random()*len);
        exp = data[experiment_number];
        condition_order = exp["condition_order"];
        num_trials = 30;
        // num_trials = 1; // Test with a smaller number of trials
        update();
      },
      error: function (err){
        console.log("error");
      }
  });
}

function debug(){
  $("#experiment_number").text("Experiment Number: " + experiment_number);
  $("#technique").text("Technique: " + technique);
  $("#condition_order").text("Condition Order: " + condition_order);
  $("#block_number").text("Block Number: " + block_number);
  $("#trial_number").text("Trial Number: " + trial_number);
  $("#correct_id").text("Correct Id: " + correct_id);
  $("#answer").text("Answer: " + answer);
  $("#num_trials").text("Num Trials: " + num_trials);
  $("#correct_word").text("Correct Word: " + correct_word);
  $("#predicted_words").text("Predicted Word: " + abrupt_onset_words);
}

function increment_numbers(){
  $(correct_id).prop("onclick", null).off("click");
  $("#menu" + correct_menu).prop("onclick", null).off("click");
  started = 0;
  if(trial_number == num_trials-1){
    trial_number = 0;
    block_number = block_number+1;
    if(block_number == 2){
      block_number = 0;
      condition = condition+1;
      if (condition == 2){
        end = 1;
      }
    }
  }
  else {
    trial_number = trial_number+1;
  }
  take_a_break_perhaps();
  if (end !== 1){
    update();
  }
}

function take_a_break_perhaps(){
  if (trial_number === 0 && block_number === 1){
    $("#prompt").hide();
    $("#experiment").hide();
    let break_number = condition+block_number;
    $(".intermediate-"+break_number).show();
  }
  else if (trial_number === 0 && block_number === 0){
    $("#prompt").hide();
    $("#experiment").hide();
    let break_number = condition+block_number;
    $(".section-break-"+break_number).show();
  }
}

function update(){
  technique = condition_order[condition];
  answer = exp["experiment_blocks"][technique][block_number]["selection_locations"][trial_number];
  let menu = answer[0]+1;
  correct_menu = menu;
  let section = Math.floor(answer[1]/4)+1;
  let item = (answer[1]%4)+1;
  correct_id = "#menu" + menu + "-section" + section + "-item" + item;
  let words = exp["experiment_blocks"][technique][block_number]["words"];
  let correct = exp["experiment_blocks"][technique][block_number]["selection_locations"][trial_number];
  let preds = exp["experiment_blocks"][technique][block_number]["predicted_locations"][trial_number];
  abrupt_onset_words = [];
  for (let i=0; i < preds.length; i++){
    let word = words[preds[i][0]][preds[i][1]];
    abrupt_onset_words.push(word);
  }
  correct_word = words[answer[0]][answer[1]];
  $("#prompt").text("Menu " + menu + " -> " + correct_word);
  change_menu(words, correct, preds);
  debug();
  set_listener();
}

function log_values(time){
  let trial = {
    "trial_number": trial_number,
    "correct_menu": correct_menu,
    "menu_index": answer[1],
    "selection_time": time,
    "condition": condition_order[condition],
    "block_number": block_number,
    "correct_word": correct_word,
    "predicted_words": abrupt_onset_words,
    "correctly_predicted": abrupt_onset_words.indexOf(correct_word) !== -1,
    "incorrect_attempts": 0,
    "incorrect_words": [],
    "incorrect_click_times":[]
  };
  data["trials"].push(trial);
}

function set_listener(){
  $(correct_id).on("click", function(){
    stop = Date.now();
    log_values(stop-start);
    increment_numbers();
  });
  $("#menu"+correct_menu).on("click", function(){
    if (started == 0){
      started = 1;
      start = Date.now();
    }
  });
}

// A function to accept an object and POST it to the server as JSON
function record_results() {
  data["condition_sequence"] = condition_order;
  data["experiment_number"] = experiment_number;
  data["number_trials"] = num_trials;
  data["qualitative_information"] = qualitative_information;

	console.log("Posting data");
	$.ajax({
		url: "/save",
		contentType: "application/json",
		type: "POST",
		data: JSON.stringify(data),
		success: function (resp) {},
		error: function (resp) {
			console.log(resp);
		}
	});
}

function end_experiment(){
  $("#experiment").hide();
  $(".end").show();
  $("#prompt").hide();
}

function save_qualitative_information(index){
  let obj = {
    "difficulty": $('#difficulty-'+index).val(),
    "efficiency": $('#efficiency-'+index).val(),
    "satisfaction": $('#satisfaction-'+index).val(),
    "frustration": $('#frustration-'+index).val()
  }
  qualitative_information[condition_order[condition-1]] = obj;
}

function overall_comparisons(){
  let demographics = {
    "age": $('#age-overall').val(),
    "gender": $('#gender-overall').val()
  };
  let overall = {
    "easy": $('#easy-overall').val(),
    "prefer": $('#prefer-overall').val()
  }
  data["demographics"] = demographics;
  data["overall-comparisons"] = overall;
}

function change_menu(words, answer, preds){
  for (let i = 0; i<words.length; i++){
    for (let j = 0; j<4; j++){
      for (let k = 0; k<4; k++){
        let menu = i+1;
        let section = j+1;
        let item = k+1
        let id = "#menu" + menu + "-section" + section + "-item" + item;
        let index = j*4+k;
        let word = words[i][index];
        $(id).text(word);
        $(id).removeClass("fading");
        if (!(abrupt_onset_words.includes(word))){
          if (technique === "ephemeral"){
            $(id).addClass("fading");
          }
        }
      }
    }
  }
}

$(document).ready(function() {
  init();
  $("#experiment").hide();
  $(".introduction").show();
  $(".intermediate-1").hide();
  $(".intermediate-2").hide();
  $(".section-break-1").hide();
  $(".section-break-2").hide();
  $(".overall-comparisons").hide();
  $(".end").hide();
  $("#log").hide();
  $("#prompt").hide();
});

$("#introduction-button").on("click", function(){
  $(".introduction").hide();
  $("#experiment").show();
  $("#prompt").show();
});

$("#intermediate-button-1").on("click", function(){
  $(".intermediate-1").hide();
  $("#experiment").show();
  $("#prompt").show();
});

$("#intermediate-button-2").on("click", function(){
  $(".intermediate-2").hide();
  $("#experiment").show();
  $("#prompt").show();
});

$("#section-break-button-1").on("click", function(){
  $(".section-break-1").hide();
  save_qualitative_information(1);
  $("#experiment").show();
  $("#prompt").show();
});

$("#section-break-button-2").on("click", function(){
  $(".section-break-2").hide();
  save_qualitative_information(2);
  $(".overall-comparisons").show();
});

$("#overall-comparisons-button").on("click", function(){
  overall_comparisons();
  record_results();
  end_experiment();
  $(".overall-comparisons").hide();
  $(".end").show();
});
