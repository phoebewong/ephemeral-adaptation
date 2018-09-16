let index = 0;

let categories = ["Fruits", "Vegetables", "Animals", "Furniture"];
let words = {
  "Fruits": ["Apple", "Banana", "Mango", "Pear"],
  "Vegetables": ["Carrot", "Celery", "Broccoli", "Cauliflower"],
  "Animals": ["Dog", "Cat", "Monkey", "Donkey"],
  "Furniture": ["Chair", "Table", "Sofa", "Desk"]
};

for (let i = 1; i<4; i++){
  for (let j = 1; j<5; j++){
    for (let k = 1; k<5; k++){
      let id = "#menu" + i + "-section" + j + "-item" + k;
      $(id).text(words[categories[j-1]][k-1]);
      if (Math.random() < 0.25){
        $(id).addClass("fading");
      }
    }
  }
}
