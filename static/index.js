var QUESTION_LIST = [
  {
    q_content: "➕",
    tag: 7597,
    test_id: "A010000060",
    assess_id: "A010060001",
    grade: 0,
  },
  {
    q_content: "➖",
    tag: 397,
    test_id: "A050000094",
    assess_id: "A050094005",
    grade: 0,
  },
  {
    q_content: "✖",
    tag: 451,
    test_id: "A050000155",
    assess_id: "A050155004",
    grade: 1,
  },
  {
    q_content: "➗",
    tag: 587,
    test_id: "A060000017",
    assess_id: "A060017006",
    grade: 2
  },
  {
    q_content: "➗",
    tag: 587,
    test_id: "A060000017",
    assess_id: "A060017007",
    grade: 3,
  }
];
var answers = [];
function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min; //최댓값도 포함, 최솟값도 포함
}

function shirink_time(time){

  function frame() {
    if (width < 0) {
      clearInterval(id);
      nextQuestion();
    } else {
      width -= 1/time;
      timebar.style.width = width + "%";
      timer.innerText= `${Math.ceil((width/100)*time)}초`
    }
  }

  var timebar = document.getElementById("time-bar");
  var timer = document.getElementById("timer");
  var width = 100
  var id = setInterval(frame, 10);
  return id
}

function nextQuestion(){
  if (isClicked) return;
  isClicked = true;
  // event.target.dataset.clicked = true;
  var answer = document.querySelector("#answer_input").value;
  var index = parseInt(document.querySelector("#q-number").innerHTML);

  answers.push(answer);
  document.querySelector("#answer_input").value = '';
  if (index == 5) {
    setTimeout(function () {
      get_score();
    }, 1000);
  } else {      
    setTimeout(function () {
      clearInterval(set_question(index));
    }, 500);
  }

  document.querySelector("#spinner").style.display = "inline-block";
  document.querySelector("#question-section").style.opacity = 0;
}

function set_question(index) {
  let q_content = QUESTION_LIST[index].q_content;
  // $('#tag').text(q_content);
  // document.querySelector("#knowledgeTag").innerText = q_content;
  document.querySelector("#q-number").innerText = index + 1;
  document.querySelector("#question-section").style.opacity = 1;
  document.getElementById("time-bar").style.width = 100 + "%";;
  var left = getRandomIntInclusive(290, 310);
  var right = getRandomIntInclusive(390, 410);
  var question = `${left} ${q_content} ${right} = ?`;
  var time = 60 - QUESTION_LIST[index].grade*5;
  document.querySelector("#question-text").innerText = question;
  document.querySelector("#spinner").style.display = "none";
  document.querySelector("#question-section").style.display = "inline-block";
  isClicked = false;
  return shirink_time(time)
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
      document.querySelector("#spinner").style.display = "none";
      document.querySelector("#question-section").style.display = "none";
      document.querySelector("#result").style.display = "block";
      if (score != 0) {
        animateValue("value", 0, JSON.stringify(response), 3000);
      }
    })
    .catch((error) => console.error("Error:", error));
}

var isClicked = false;
document.querySelector('#start_btn').addEventListener("click", function(event){
  document.querySelector("#question-section").dataset.started = true;
  document.querySelector("#start_quiz").style.display = "none";
  document.querySelector("#spinner").style.display = "inline-block";
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
