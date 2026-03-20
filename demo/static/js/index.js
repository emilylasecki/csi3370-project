console.log("index.js loaded");

// =========================
// FETCH TASKS FROM BACKEND
// =========================
async function fetchTasks() {
    console.log("Fetching tasks...");

    try {
        const response = await fetch("/tasks");

        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }

        const tasks = await response.json();
        console.log("Tasks received:", tasks);

        displayTasks(tasks);

    } catch (err) {
        console.error("Fetch error:", err);
    }
}


// =========================
// DISPLAY TASKS
// =========================
function displayTasks(tasks) {
    const dl = document.querySelector("#tasks dl");

    if (!dl) {
        console.error("No <dl> found inside #tasks");
        return;
    }

    // Clear placeholder content
    dl.innerHTML = "";

    tasks.forEach(task => {
        const dt = document.createElement("dt");
        dt.textContent = task.taskName || "No title";

        const dd = document.createElement("dd");
        dd.textContent =
            (task.description || "") +
            " — Due: " + (task.dueDate || "") +
            " [" + (task.status || "") + "]" +
            " [" + (task.effortEstimation || "") + "]" +
            " [" + (task.priority || "") + "]";

        dl.appendChild(dt);
        dl.appendChild(dd);
    });
}


// =========================
// RUN ON PAGE LOAD
// =========================
fetchTasks();