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

function init(){
  $.get({
      url: "expt_generation/experiment_data.json",
      success: function (data) {
        console.log(data);
        let len = data.length;
        experiment_number = Math.floor(Math.random()*len);
        exp = data[experiment_number];
        condition_order = exp["condition_order"];
        num_trials = exp["predicted_locations"].length;
        // num_trials = 4; // Test with a smaller number of trials
        update();
      },
      error: function (err){
        console.log("error");
      }
  });
}

function log(){
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
  if(trial_number == num_trials-1){
    trial_number = 0;
    block_number = block_number+1;
    if(block_number == 2){
      block_number = 0;
      condition = condition+1;
      if (condition == 2){
        console.log("END");
        end = 1;
      }
    }
  }
  else {
    trial_number = trial_number+1;
  }
  if (end !== 1){
    update();
  }
}

function update(){
  technique = condition_order[condition];
  answer = exp["selection_locations"][trial_number];
  let menu = answer[0]+1;
  let section = Math.floor(answer[1]/4)+1;
  let item = (answer[1]%4)+1;
  correct_id = "#menu" + menu + "-section" + section + "-item" + item;
  let words = exp["experiment_blocks"][technique][block_number]["words"];
  let correct = exp["selection_locations"][trial_number];
  let preds = exp["predicted_locations"][trial_number];
  abrupt_onset_words = [];
  for (let i=0; i < preds.length; i++){
    let word = words[preds[i][0]][preds[i][1]];
    abrupt_onset_words.push(word);
  }
  correct_word = words[answer[0]][answer[1]];
  $("#prompt").text("Menu " + menu + " -> " + correct_word);
  change_menu(words, correct, preds);
  log();
  set_listener();
}

function set_listener(){
  $(correct_id).on("click", function(){
    console.log("clicked");
    increment_numbers();
  });
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
});
