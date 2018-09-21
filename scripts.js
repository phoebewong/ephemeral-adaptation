$.get({
    url: "expt_generation/experiment_data.json",
    success: function (data) {
      console.log(data);
      var exp = data[0];
      changeMenu(exp["experiment_blocks"]["control"][0], exp["selection_locations"][0], exp["predicted_locations"][0]);
    },
    error: function (err){
      console.log("error");
    }
});

function changeMenu(all_words, answer, preds){
  words = all_words["words"];

  for (let i = 0; i<words.length; i++){
    for (let j = 0; j<4; j++){
      for (let k = 0; k<4; k++){
        let id = "#menu" + (i+1) + "-section" + (j+1) + "-item" + (k+1);
        let index = j*4+k;
        $(id).text(words[i][index]);
        if (i==answer[0] && index == answer[1]){
          $(id).css("color","blue");
        }
      }
    }
  }
}
