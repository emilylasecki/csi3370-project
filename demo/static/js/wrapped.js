const currentMonth = new Date().toLocaleString("default", { month: "long" });

const backendData = typeof wrapDataFromBackend !== "undefined" ? wrapDataFromBackend : {};
const isWrapLocked = typeof wrapLocked !== "undefined" ? wrapLocked : false;
const tasksNeededCount = typeof tasksNeeded !== "undefined" ? tasksNeeded : 0;

console.log("BACKEND DATA:", backendData);
console.log("WRAP LOCKED:", isWrapLocked);
console.log("TASKS NEEDED:", tasksNeededCount);

const wrappedData = [
  {
    title: "Total Tasks",
    value: `${backendData.total_tasks ?? 0} Tasks`,
    stat: `You created ${backendData.total_tasks ?? 0} tasks`,
    comments: [
      "Every big result starts with one task.",
      "You gave yourself goals to work on.",
      "Your month had a full to-do list.",
      "You kept yourself busy this month."
    ],
    candy: "🍬",
    theme: "card-theme-ocean",
    candyClass: "candy-blue",
    fruits: ["🫐", "🍏", "🍎", "🍒"]
  },
  {
    title: "Completed Tasks",
    value: `${backendData.completed_tasks ?? 0} Done`,
    stat: `You completed ${backendData.completed_tasks ?? 0} tasks`,
    comments: [
      "Finished tasks always feel satisfying.",
      "Progress was definitely made.",
      "You got important things done.",
      "That checklist got shorter."
    ],
    candy: "🍭",
    theme: "card-theme-lemon",
    candyClass: "candy-yellow",
    fruits: ["🍋", "🍌", "🍍", "🍊"]
  },
  {
    title: "Completion Rate",
    value: `${backendData.completion_rate ?? 0}%`,
    stat: `Your completion rate was ${backendData.completion_rate ?? 0}%`,
    comments: [
      "Consistency builds momentum.",
      "Every finished task counts.",
      "Small wins add up over time.",
      "You are building stronger habits."
    ],
    candy: "🍪",
    theme: "card-theme-mint",
    candyClass: "candy-green",
    fruits: ["🥝", "🍐", "🍇", "🍈"]
  },
  {
    title: "Top Priority Type",
    value: `${backendData.top_priority ?? "None"}`,
    stat: `Most of your tasks were ${backendData.top_priority ?? "None"} priority`,
    comments: [
      "Your priorities shaped your month.",
      "You focused on what seemed most important.",
      "Priority choices say a lot about your workflow.",
      "Your task style is starting to show."
    ],
    candy: "🍫",
    theme: "card-theme-lavender",
    candyClass: "candy-purple",
    fruits: ["🍇", "🫐", "🍉", "🍒"]
  },
  {
    title: "Overdue Tasks",
    value: `${backendData.overdue_tasks ?? 0}`,
    stat: `You had ${backendData.overdue_tasks ?? 0} overdue tasks`,
    comments: [
      "A few missed deadlines happen to everyone.",
      "This is a good spot to improve next month.",
      "Try breaking tasks into smaller parts next time.",
      "Deadlines are easier when tasks feel smaller."
    ],
    candy: "🧁",
    theme: "card-theme-sunset",
    candyClass: "candy-orange",
    fruits: ["🍊", "🥭", "🍑", "🍓"]
  }
];

let currentIndex = -1;
let giftOpened = false;

function getRandomComment(comments) {
  return comments[Math.floor(Math.random() * comments.length)];
}

function showScreen(screenId) {
  document.querySelectorAll(".screen").forEach((screen) => {
    screen.classList.remove("active");
  });

  const targetScreen = document.getElementById(screenId);
  if (targetScreen) {
    targetScreen.classList.add("active");
  }
}

function ensureGlobalConfetti() {
  document.querySelectorAll(".global-confetti").forEach((el) => el.remove());

  document.querySelectorAll(".screen").forEach((screen) => {
    const wrap = document.createElement("div");
    wrap.className = "global-confetti";

    const classes = [
      "one", "two", "three", "four",
      "five", "six", "seven", "eight",
      "nine", "ten", "eleven", "twelve",
      "thirteen", "fourteen", "fifteen", "sixteen"
    ];

    classes.forEach((name) => {
      const piece = document.createElement("div");
      piece.className = `confetti-drop ${name}`;
      wrap.appendChild(piece);
    });

    screen.prepend(wrap);
  });
}

function ensureInnerConfetti() {
  document.querySelectorAll(".card-confetti").forEach((el) => el.remove());

  const targets = [
    document.getElementById("storyCard"),
    document.getElementById("summaryCard")
  ];

  targets.forEach((target) => {
    if (!target) return;

    const wrap = document.createElement("div");
    wrap.className = "card-confetti";

    const classes = ["one", "two", "three", "four", "five", "six"];

    classes.forEach((name) => {
      const piece = document.createElement("div");
      piece.className = `card-confetti-piece ${name}`;
      wrap.appendChild(piece);
    });

    target.prepend(wrap);
  });
}

function launchBowAway() {
  const giftStage = document.getElementById("giftStage");
  if (!giftStage) return;

  const bowFly = document.createElement("div");
  bowFly.className = "bow-fly-away";

  const left = document.createElement("div");
  left.className = "fly-left";

  const right = document.createElement("div");
  right.className = "fly-right";

  const knot = document.createElement("div");
  knot.className = "fly-knot";

  bowFly.appendChild(left);
  bowFly.appendChild(right);
  bowFly.appendChild(knot);

  giftStage.appendChild(bowFly);

  setTimeout(() => {
    bowFly.remove();
  }, 1100);
}

function openGiftBox() {
  if (isWrapLocked) return;
  if (giftOpened) return;

  giftOpened = true;

  const giftStage = document.getElementById("giftStage");
  const continueRow = document.getElementById("giftContinueRow");
  const mainTitle = document.getElementById("mainTitle");

  if (giftStage) {
    giftStage.classList.add("open");
  }

  if (mainTitle) {
    mainTitle.textContent = `${currentMonth} Wrapped is here`;
  }

  setTimeout(() => {
    launchBowAway();
  }, 120);

  setTimeout(() => {
    if (continueRow) {
      continueRow.style.display = "flex";
    }
  }, 900);
}

function startWrappedStory() {
  if (isWrapLocked) return;

  currentIndex = 0;
  renderCard(true);
  showScreen("cardScreen");
}

function renderFruitFloor(fruits) {
  const fruitFloor = document.getElementById("fruitFloor");
  if (!fruitFloor) return;

  fruitFloor.innerHTML = "";

  const classes = ["left-one", "left-two", "right-one", "right-two"];

  fruits.forEach((fruit, index) => {
    const fruitEl = document.createElement("div");
    fruitEl.className = `fruit-piece ${classes[index]}`;
    fruitEl.textContent = fruit;
    fruitEl.style.animationDelay = `${index * 0.5}s`;
    fruitFloor.appendChild(fruitEl);
  });
}

function renderCard(animate = false) {
  if (isWrapLocked) return;

  const item = wrappedData[currentIndex];
  if (!item) return;

  const comment = getRandomComment(item.comments);

  const cardTitle = document.getElementById("cardTitle");
  const cardValue = document.getElementById("cardValue");
  const cardStat = document.getElementById("cardStat");
  const cardComment = document.getElementById("cardComment");
  const candyEmoji = document.getElementById("candyEmoji");

  if (cardTitle) cardTitle.textContent = `${currentMonth} Wrapped • ${item.title}`;
  if (cardValue) cardValue.textContent = item.value;
  if (cardStat) cardStat.textContent = item.stat;
  if (cardComment) cardComment.textContent = comment;
  if (candyEmoji) candyEmoji.textContent = item.candy;

  const card = document.getElementById("storyCard");
  if (card) {
    card.className = `story-card ${item.theme}`;
  }

  const leftCandy = document.getElementById("leftCandy");
  const rightCandy = document.getElementById("rightCandy");

  if (leftCandy) leftCandy.className = `candy-piece candy-left ${item.candyClass}`;
  if (rightCandy) rightCandy.className = `candy-piece candy-right ${item.candyClass}`;

  renderFruitFloor(item.fruits);
  ensureInnerConfetti();

  if (animate && card) {
    card.style.animation = "none";
    void card.offsetWidth;
    card.style.animation = "cardRise 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)";
  }

  const nextBtn = document.getElementById("nextBtn");
  if (nextBtn) {
    nextBtn.textContent = currentIndex === wrappedData.length - 1 ? "Final Summary" : "Next";
  }
}

function goNext() {
  if (isWrapLocked) return;

  if (currentIndex < wrappedData.length - 1) {
    currentIndex++;
    renderCard(true);
  } else {
    renderSummary();
    showScreen("summaryScreen");
  }
}

function goBack() {
  if (isWrapLocked) return;

  const summaryScreen = document.getElementById("summaryScreen");

  if (summaryScreen && summaryScreen.classList.contains("active")) {
    currentIndex = wrappedData.length - 1;
    renderCard(true);
    showScreen("cardScreen");
    return;
  }

  if (currentIndex > 0) {
    currentIndex--;
    renderCard(true);
  } else {
    showScreen("giftScreen");
  }
}

function renderSummary() {
  if (isWrapLocked) return;

  const summaryContent = document.getElementById("summaryContent");
  if (!summaryContent) return;

  summaryContent.innerHTML = `
    <div class="summary-line">
      <strong>Total Tasks:</strong> ${backendData.total_tasks ?? 0}<br>
      You created ${backendData.total_tasks ?? 0} tasks
    </div>

    <div class="summary-line">
      <strong>Completed Tasks:</strong> ${backendData.completed_tasks ?? 0}<br>
      You completed ${backendData.completed_tasks ?? 0} tasks
    </div>

    <div class="summary-line">
      <strong>In Progress:</strong> ${backendData.in_progress_tasks ?? 0}<br>
      Tasks still being worked on
    </div>

    <div class="summary-line">
      <strong>Not Started:</strong> ${backendData.not_started_tasks ?? 0}<br>
      Tasks you have not started yet
    </div>

    <div class="summary-line">
      <strong>Overdue Tasks:</strong> ${backendData.overdue_tasks ?? 0}<br>
      Tasks that passed their due date
    </div>

    <div class="summary-line">
      <strong>Summary:</strong> ${backendData.summary_message ?? "No summary available"}
    </div>
  `;

  ensureInnerConfetti();
}

function replayWrapped() {
  if (isWrapLocked) return;

  currentIndex = -1;
  giftOpened = false;

  showScreen("giftScreen");

  const giftStage = document.getElementById("giftStage");
  const continueRow = document.getElementById("giftContinueRow");
  const mainTitle = document.getElementById("mainTitle");

  if (giftStage) {
    giftStage.classList.remove("open");
  }

  if (continueRow) {
    continueRow.style.display = "none";
  }

  if (mainTitle) {
    mainTitle.textContent = "Open Your Monthly Wrapped";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  ensureGlobalConfetti();
  ensureInnerConfetti();
});