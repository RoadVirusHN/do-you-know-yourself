var section_ids = [
  "#result",
  "#question-section",
  "#start_quiz",
  "#spinner"
]
var QUESTION_LIST = [];
fetch("/get_questions")
.then((res) => res.json())
  .then((response) => {
    // console.log(typeof(response))
    for (const k in response){
      QUESTION_LIST.push(response[k]);
    }
    // QUESTION_LIST = response.map(x=>response[x]);
    // console.log(QUESTION_LIST)
    unset_loading("#start_quiz");
  })
  .catch((error) => console.error("Error:", error));

set_loading();
var isClicked = false;
var answers = [];

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min; //최댓값도 포함, 최솟값도 포함
}

function set_loading() {
  for (let section of section_ids){
    document.querySelector(section).style.display = "none";
  }
  document.querySelector("#spinner").style.display = "inline-block";
  console.log(document.querySelector("#spinner").style.display)
}

function unset_loading(ids){  
  document.querySelector("#spinner").style.display = "none";
  document.querySelector(ids).style.display = "inline-block";
}

// function shirink_time(time){
//   function frame() {
//     if (width < 0) {
//       clearInterval(id);
//       nextQuestion();
//     } else {
//       width -= 1/time;
//       timebar.style.width = width + "%";
//       timer.innerText= `${Math.ceil((width/100)*time)}초`
//     }
//   }

//   var timebar = document.getElementById("time-bar");
//   var timer = document.getElementById("timer");
//   var width = 100
//   var id = setInterval(frame, 10);
//   return id
// }

function nextQuestion(){
  if (isClicked) return;
  isClicked = true;
  // event.target.dataset.clicked = true;
  var answer = document.querySelector("#answer_input").value;
  var index = parseInt(document.querySelector("#q-number").innerText);
  answers.push(answer);
  document.querySelector("#answer_input").value = '';
  
  if (index == QUESTION_LIST.length) {
    setTimeout(function () {
      get_score();
    }, 1000);
  } else {      
    document.querySelector('#q_num').innerText = `${index+1}/${QUESTION_LIST.length}`
    setTimeout(function () {
      clearInterval(set_question(index));
    }, 500);
  }

  document.querySelector("#spinner").style.display = "inline-block";
  document.querySelector("#question-section").style.opacity = 0;
}


function set_question(index) {
  let question = QUESTION_LIST[index].text;
  document.querySelector("#q-number").innerText = index + 1;
  document.querySelector("#question-section").style.opacity = 1;
  
  document.querySelector("#question-text").innerText = question;
  unset_loading("#question-section");
  isClicked = false;
  
  // document.getElementById("time-bar").style.width = 100 + "%";  
  // var time = 40 - QUESTION_LIST[index].grade*10;
  // return shirink_time(time)
}

function get_score() {
  for (var i = 0; i < QUESTION_LIST.length; i++) {
    QUESTION_LIST[i]["answer"] = answers[i];
  }

  fetch("/get_score", {
    method: "POST", // or 'PUT'
    body: JSON.stringify(QUESTION_LIST), // data can be `string` or {object}!
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((response) => {
      var score = parseInt(JSON.stringify(response));
      unset_loading("#result");
      document.querySelector("#question-section").style.display = "none";
      if (score != 0) {
        animateValue("value", 0, JSON.stringify(response), 3000);
      }
    })
    .catch((error) => console.error("Error:", error));
}

document.querySelector('#start_btn').addEventListener("click", function(event){
  document.querySelector("#question-section").dataset.started = true;
  document.querySelector("#start_quiz").style.display = "none";
  document.querySelector('#q_num').innerText = `${1}/${QUESTION_LIST.length}`
  set_loading();
  set_question(0);  
})

document.querySelector('#answer-btn').addEventListener("click", function (event) {
  nextQuestion()
});

document.querySelector('#restart-btn').addEventListener("click", function (event) {
  window.location.reload()
});

function animateValue(id, start, end, duration) {
  if (start === end) return;
  var range = end - start;
  var current = start;
  var increment = end > start ? 1 : -1;
  var stepTime = Math.abs(Math.floor(duration / range));
  var obj = document.getElementById(id);
  var timer = setInterval(function () {
    current += increment;
    obj.innerHTML = current;
    if (current == end) {
      clearInterval(timer);
    }
  }, stepTime);
}
