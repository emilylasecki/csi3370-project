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
    fruits: ["🫐", "🍏"]
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
    fruits: ["🍋", "🍌"]
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
    candy: "🍬",
    theme: "card-theme-mint",
    candyClass: "candy-green",
    fruits: ["🥝", "🍐"]
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
    fruits: ["🍇", "🫐"]
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
    candy: "🍬",
    theme: "card-theme-sunset",
    candyClass: "candy-orange",
    fruits: ["🍊", "🥭"]
  }
];

let currentIndex = -1;
let giftOpened = false;

function getRandomComment(comments) {
  return comments[Math.floor(Math.random() * comments.length)];
}

function showScreen(screenId) {
  document.querySelectorAll(".screen").forEach(screen => {
    screen.classList.remove("active");
  });
  document.getElementById(screenId).classList.add("active");
}

function openGiftBox() {
  if (giftOpened) return;

  giftOpened = true;

  const giftStage = document.getElementById("giftStage");
  const continueRow = document.getElementById("giftContinueRow");
  const mainTitle = document.getElementById("mainTitle");

  giftStage.classList.add("open");
  mainTitle.textContent = `${currentMonth} Wrapped is here`;

  setTimeout(() => {
    continueRow.style.display = "flex";
  }, 900);
}

function startWrappedStory() {
  currentIndex = 0;
  renderCard(true);
  showScreen("cardScreen");
}

function ensureGlobalConfetti() {
  document.querySelectorAll(".global-confetti").forEach(el => el.remove());

  document.querySelectorAll(".screen").forEach(screen => {
    const wrap = document.createElement("div");
    wrap.className = "global-confetti";

    const classes = ["one","two","three","four","five","six","seven","eight","nine","ten"];

    classes.forEach(name => {
      const piece = document.createElement("div");
      piece.className = `confetti-drop ${name}`;
      wrap.appendChild(piece);
    });

    screen.prepend(wrap);
  });
}

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

  let fruitLeft = document.getElementById("fruitLeft");
  let fruitRight = document.getElementById("fruitRight");

  if (!fruitLeft) {
    fruitLeft = document.createElement("div");
    fruitLeft.id = "fruitLeft";
    fruitLeft.className = "fruit-piece fruit-left";
    card.appendChild(fruitLeft);
  }

  if (!fruitRight) {
    fruitRight = document.createElement("div");
    fruitRight.id = "fruitRight";
    fruitRight.className = "fruit-piece fruit-right";
    card.appendChild(fruitRight);
  }

  fruitLeft.textContent = item.fruits[0];
  fruitRight.textContent = item.fruits[1];

  const oldDrinkLeft = document.getElementById("drinkLeft");
  const oldDrinkRight = document.getElementById("drinkRight");

  if (oldDrinkLeft) oldDrinkLeft.remove();
  if (oldDrinkRight) oldDrinkRight.remove();

  if (animate) {
    card.style.animation = "none";
    void card.offsetWidth;
    card.style.animation = "flipIn 0.65s ease";
  }

  const nextBtn = document.getElementById("nextBtn");
  nextBtn.textContent = currentIndex === wrappedData.length - 1 ? "Final Summary" : "Next";
}

function goNext() {
  if (currentIndex < wrappedData.length - 1) {
    currentIndex++;
    renderCard(true);
  } else {
    renderSummary();
    showScreen("summaryScreen");
  }
}

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

function renderSummary() {
  const summaryContent = document.getElementById("summaryContent");

  summaryContent.innerHTML = wrappedData.map(item => `
    <div class="summary-line">
      <strong>${item.title}:</strong> ${item.value}<br>
      ${item.stat}
    </div>
  `).join("");
}

document.addEventListener("DOMContentLoaded", () => {
  ensureGlobalConfetti();
});