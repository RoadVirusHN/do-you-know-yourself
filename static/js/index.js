var section_ids = ["#result", "#question-section", "#start_quiz", "#spinner"];
var QUESTION_LIST = [];
var user_id, tag;
var start;
var end;

const spinner = document.querySelector("#spinner");
const answer_input = document.querySelector("#answer_input");
const question_section = document.querySelector("#question-section");

const answer_button = document.querySelector("#answer-btn");
answer_button.addEventListener("click", function (event) {
  end = new Date();
  nextQuestion();
});

document
  .querySelector("#restart-btn")
  .addEventListener("click", function (event) {
    window.location.reload();
  });

const user_input = document.querySelector("#user_input");
user_input.addEventListener("input", function (event) {
  user_id = user_input.value;
  if (user_input.value.length > 2 && tag_input.value) {
    start_btn.disabled = false;
  } else {
    start_btn.disabled = true;
  }
});

const tag_input = document.querySelector("#tag_input");
tag_input.addEventListener("change", function (event) {
  tag = tag_input.value;
  if (user_input.value.length > 2 && tag_input.value) {
    start_btn.disabled = false;
  } else {
    start_btn.disabled = true;
  }
});

const indicator = document.querySelector("#indicator");
const start_btn = document.querySelector("#start_btn");
start_btn.addEventListener("click", function (event) {
  question_section.dataset.started = true;
  document.querySelector("#start_quiz").style.display = "none";
  user_id = user_input.value;
  tag = tag_input.value;
  set_loading();
  fetch("/get_questions", {
    method: "POST",
    body: JSON.stringify({ tag: tag, user: user_id }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((response) => {
      for (const k in response) {
        QUESTION_LIST.push(response[k]);
      }
      document.querySelector("#q_num").innerText = `${1}/${QUESTION_LIST.length
        }`;
      console.log(QUESTION_LIST)
      set_question(0);
      indicator.innerText = "⚪".repeat(QUESTION_LIST.length);
      document.addEventListener("keydown", function (event) {
        if (
          event.key == "1" ||
          event.key == "2" ||
          event.key == "3" ||
          event.key == "4"
        ) {
          answer_input.options.value = parseInt(event.key) - 1;
          document.querySelector(`#choice${parseInt(event.key) - 1}`).click();
        } else if (event.key == "Enter" || event.key == " ") {
          answer_button.click();
        }
      });
    })
    .catch((error) => console.error("Error:", error));
});

var isClicked = false;
var answers = [];
var userID = [];
var elapsed = [];
function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min; //최댓값도 포함, 최솟값도 포함
}

function set_loading() {
  for (let section of section_ids) {
    document.querySelector(section).style.display = "none";
  }
  spinner.style.display = "inline-block";
}

function unset_loading(ids) {
  spinner.style.display = "none";
  document.querySelector(ids).style.display = "inline-block";
}

function nextQuestion() {
  if (isClicked) return;
  isClicked = true;
  // event.target.dataset.clicked = true;
  var answer = parseInt(answer_input.options.value);
  var index = parseInt(document.querySelector("#q-number").innerText);
  var real_index = index - 1;
  answers.push(answer);
  answer_input.options.value = "";
  if (answer == QUESTION_LIST[real_index]["answer"]) {
    QUESTION_LIST[real_index]["user_answer"] = 1;
    indicator.innerText = indicator.innerText.replace("⚪", "🟢");
  } else {
    QUESTION_LIST[real_index]["user_answer"] = 0;
    indicator.innerText = indicator.innerText.replace("⚪", "🔴");
  }
  QUESTION_LIST[real_index]["user_id"] = user_id;
  QUESTION_LIST[real_index]["tag"] = tag;
  QUESTION_LIST[real_index]['Timestamp'] = (new Date()).getTime();
  QUESTION_LIST[real_index]["elapsed"] = end - start;

  if (index == QUESTION_LIST.length) {
    setTimeout(function () {
      get_score();
    }, 1000);
  } else {
    document.querySelector("#q_num").innerText = `${index + 1}/${QUESTION_LIST.length
      }`;
    setTimeout(function () {
      clearInterval(set_question(index));
    }, 500);
  }

  spinner.style.display = "inline-block";
  question_section.style.opacity = 0;
}

function set_question(index) {
  let question = QUESTION_LIST[index].text;
  console.log(QUESTION_LIST["choices"]);
  document.querySelector("#q-number").innerText = index + 1;
  question_section.style.opacity = 1;
  for (var i of [0, 1, 2, 3]) {
    document.querySelector(`#choice${i}`).innerText =
      QUESTION_LIST[index][`choice${i}`];
  }
  document.querySelector("#question-text").innerText = question;

  unset_loading("#question-section");
  answer_input.autofocus = true;
  isClicked = false;
  start = new Date();
}
function embed_card(card_name, data) {
  card = document.querySelector(card_name);
  const card_title = card.querySelector(".card-title");
  const user_name = card.querySelector("#user_name");
  const hidden_answer = card.querySelector(".hidden_answer");
  const hidden_answer_btn = card.querySelector(".hidden_answer_btn");
  card_title.innerText = data["text"];
  user_name.innerText = user_id;
  hidden_answer.innerText = parseInt(data["answer"])+1;

  hidden_answer_btn.addEventListener("click", function (event) {
    hidden_answer.hidden = false;
    hidden_answer_btn.hidden = true;
  });
  for (var i of [0, 1, 2, 3]) {
    card.querySelector(`.card_choice${i}`).innerText = data[`choice${i}`];
  }
}
function get_score() {
  fetch("/get_score", {
    method: "POST", // or 'PUT'
    body: JSON.stringify(QUESTION_LIST), // data can be `string` or {object}!
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((response) => {
      var data = response;
      unset_loading("#result");
      question_section.style.display = "none";
      document.querySelector('#real_result').innerText = `${QUESTION_LIST.filter(function(item){
        return item['user_answer'];
      }).length}/${QUESTION_LIST.length}`
      document.querySelector("#all_len").innerText = `${tag_input.options[parseInt(tag) + 1].innerText
        } 분야 ${data["tag_problem_len"]} 문제 중에 `;
      if (data["score"] != 0) {
        animateValue("value", 0, data["score"], 3000);
      }
      embed_card("#hard_card", data["h_problem"]);
      embed_card("#easy_card", data["e_problem"]);
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
