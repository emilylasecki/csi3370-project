const currentMonth = new Date().toLocaleString("default", { month: "long" });

const wrappedData = [
  {
    title: "Total Tasks Completed",
    value: "42 Tasks",
    stat: "You finished 42 tasks this month",
    comments: [
      "Your to-do list did not stand a chance.",
      "Productivity level: impressive.",
      "That checklist got WORKED this month.",
      "You really showed those tasks who is boss."
    ],
    candy: "🍬",
    theme: "card-theme-ocean",
    candyClass: "candy-blue",
    fruits: ["🫐", "🍏", "🍎", "🍒"]
  },
  {
    title: "Most Productive Day",
    value: "Tuesday",
    stat: "You completed 11 tasks on Tuesday",
    comments: [
      "Apparently Tuesdays are your main character moment.",
      "Tuesday really came through for you.",
      "That day was carrying the whole month.",
      "Tuesday was clearly in its productive era."
    ],
    candy: "🍭",
    theme: "card-theme-lemon",
    candyClass: "candy-yellow",
    fruits: ["🍋", "🍌", "🍍", "🍊"]
  },
  {
    title: "Top Task Category",
    value: "School",
    stat: "48% of your completed tasks were School tasks",
    comments: [
      "Academic weapon energy detected.",
      "Your planner basically turned into a study guide.",
      "Brains were definitely in use this month.",
      "School tasks stayed at the top of the leaderboard."
    ],
    candy: "🍪",
    theme: "card-theme-mint",
    candyClass: "candy-green",
    fruits: ["🥝", "🍐", "🍇", "🍈"]
  },
  {
    title: "Longest Streak",
    value: "6 Days",
    stat: "You completed tasks 6 days in a row",
    comments: [
      "Consistency unlocked.",
      "That streak deserves a tiny celebration.",
      "Momentum was definitely on your side.",
      "Six days of focus is actually iconic."
    ],
    candy: "🍫",
    theme: "card-theme-lavender",
    candyClass: "candy-purple",
    fruits: ["🍇", "🫐", "🍉", "🍒"]
  },
  {
    title: "Your Task Style",
    value: "Night Owl Worker",
    stat: "41% of your tasks were completed after 9 PM",
    comments: [
      "Late night productivity arc activated.",
      "The moon witnessed most of your achievements.",
      "Night shift but make it productive.",
      "Some people sleep. You complete tasks."
    ],
    candy: "🧁",
    theme: "card-theme-sunset",
    candyClass: "candy-orange",
    fruits: ["🍊", "🥭", "🍑", "🍓"]
  }
];

let currentIndex = -1;
let giftOpened = false;

/* picks one random comment */
function getRandomComment(comments) {
  return comments[Math.floor(Math.random() * comments.length)];
}

/* shows only one screen */
function showScreen(screenId) {
  document.querySelectorAll(".screen").forEach((screen) => {
    screen.classList.remove("active");
  });

  document.getElementById(screenId).classList.add("active");
}

/* adds falling confetti to all screens */
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

/* adds falling confetti inside the card and summary */
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

/* makes the bow fly up and away */
function launchBowAway() {
  const giftStage = document.getElementById("giftStage");

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

/* opens gift only one time */
function openGiftBox() {
  if (giftOpened) return;

  giftOpened = true;

  const giftStage = document.getElementById("giftStage");
  const continueRow = document.getElementById("giftContinueRow");
  const mainTitle = document.getElementById("mainTitle");

  giftStage.classList.add("open");
  mainTitle.textContent = `${currentMonth} Wrapped is here`;

  setTimeout(() => {
    launchBowAway();
  }, 120);

  setTimeout(() => {
    continueRow.style.display = "flex";
  }, 900);
}

/* starts the story from first card */
function startWrappedStory() {
  currentIndex = 0;
  renderCard(true);
  showScreen("cardScreen");
}

/* shows 4 fruits, 2 on each side */
function renderFruitFloor(fruits) {
  const fruitFloor = document.getElementById("fruitFloor");
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

/* fills the current card */
function renderCard(animate = false) {
  const item = wrappedData[currentIndex];
  const comment = getRandomComment(item.comments);

  document.getElementById("cardTitle").textContent = `${currentMonth} Wrapped • ${item.title}`;
  document.getElementById("cardValue").textContent = item.value;
  document.getElementById("cardStat").textContent = item.stat;
  document.getElementById("cardComment").textContent = comment;
  document.getElementById("candyEmoji").textContent = item.candy;

  const card = document.getElementById("storyCard");
  card.className = `story-card ${item.theme}`;

  const leftCandy = document.getElementById("leftCandy");
  const rightCandy = document.getElementById("rightCandy");

  leftCandy.className = `candy-piece candy-left ${item.candyClass}`;
  rightCandy.className = `candy-piece candy-right ${item.candyClass}`;

  renderFruitFloor(item.fruits);
  ensureInnerConfetti();

  if (animate) {
    card.style.animation = "none";
    void card.offsetWidth;
    card.style.animation = "cardRise 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)";
  }

  const nextBtn = document.getElementById("nextBtn");
  nextBtn.textContent = currentIndex === wrappedData.length - 1 ? "Final Summary" : "Next";
}

/* goes to next card or final summary */
function goNext() {
  if (currentIndex < wrappedData.length - 1) {
    currentIndex++;
    renderCard(true);
  } else {
    renderSummary();
    showScreen("summaryScreen");
  }
}

/* goes back one screen */
function goBack() {
  if (document.getElementById("summaryScreen").classList.contains("active")) {
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

/* builds final summary */
function renderSummary() {
  const summaryContent = document.getElementById("summaryContent");

  summaryContent.innerHTML = wrappedData.map((item) => `
    <div class="summary-line">
      <strong>${item.title}:</strong> ${item.value}<br>
      ${item.stat}
    </div>
  `).join("");

  ensureInnerConfetti();
}

/* runs once on page load */
document.addEventListener("DOMContentLoaded", () => {
  ensureGlobalConfetti();
  ensureInnerConfetti();
});