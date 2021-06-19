var section_ids = [
  "#result",
  "#question-section",
  "#start_quiz",
  "#spinner"
]
var QUESTION_LIST = [];
var user_id;


const spinner = document.querySelector("#spinner");
const answer_input = document.querySelector("#answer_input");
const question_section= document.querySelector("#question-section");

const answer_button = document.querySelector('#answer-btn');
answer_button.addEventListener("click", function (event) {
  nextQuestion()
});

document.querySelector('#restart-btn').addEventListener("click", function (event) {
  window.location.reload()
});

const user_input = document.querySelector('#user_input');
user_input.addEventListener("input", function(event){
  if (user_input.value.length > 2){
    start_btn.disabled = false;
  } else {
    start_btn.disabled = true;
  }
});


const start_btn = document.querySelector('#start_btn');
start_btn.addEventListener("click", function(event){
  question_section.dataset.started = true;
  document.querySelector("#start_quiz").style.display = "none";
  set_loading();
  fetch("/get_questions", {
    method: "POST",
    body:  JSON.stringify({tag:'0', user:user_input.value}), 
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then((res) => res.json())
  .then((response) => {
    console.log(response)
    for (const k in response){
      QUESTION_LIST.push(response[k]);
    }
    document.querySelector('#q_num').innerText = `${1}/${QUESTION_LIST.length}`
    set_question(0);  
  })
  .catch((error) => console.error("Error:", error));  
});

var isClicked = false;
var answers = [];

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min; //최댓값도 포함, 최솟값도 포함
}

function set_loading() {
  for (let section of section_ids) {
    document.querySelector(section).style.display = "none";
  }
  spinner.style.display = "inline-block"
}

function unset_loading(ids){  
  spinner.style.display = "none";
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

function nextQuestion() {
  if (isClicked) return;
  isClicked = true;
  // event.target.dataset.clicked = true;
  var answer = answer_input.value;
  var index = parseInt(document.querySelector("#q-number").innerText);
  answers.push(answer);
  answer_input.value = '';
  
  if (index == QUESTION_LIST.length) {
    setTimeout(function () {
      get_score();
    }, 1000);
  } else {
    document.querySelector('#q_num').innerText = `${index + 1}/${QUESTION_LIST.length}`
    setTimeout(function () {
      clearInterval(set_question(index));
    }, 500);
  }

  spinner.style.display = "inline-block";
  question_section.style.opacity = 0;
}

function set_question(index) {
  let question = QUESTION_LIST[index].text;
  document.querySelector("#q-number").innerText = index + 1;
  question_section.style.opacity = 1;
  
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
      question_section.style.display = "none";
      if (score != 0) {
        animateValue("value", 0, JSON.stringify(response), 3000);
      }
    })
    .catch((error) => console.error("Error:", error));
}

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
