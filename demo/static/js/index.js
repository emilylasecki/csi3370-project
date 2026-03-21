console.log("index.js loaded");

let currentFilter = "none"; // global filter state

async function fetchTasks() {
    try {
        const response = await fetch("/tasks");
        if (!response.ok) throw new Error("Failed to fetch tasks");

        const tasks = await response.json();
        console.log("Tasks received:", tasks);

        // Apply the current filter before displaying
        const filteredTasks = applyFilter(tasks, currentFilter);

        displayTasks(filteredTasks);

    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function applyFilter(tasks, filter) {
    switch (filter) {
        case "priority":
            return tasks.sort((a, b) => (b.priority || 0) - (a.priority || 0));
        case "due":
            return tasks.sort((a, b) => {
                const dateA = a.dueDate ? new Date(a.dueDate) : new Date(9999, 0);
                const dateB = b.dueDate ? new Date(b.dueDate) : new Date(9999, 0);
                return dateA - dateB;
            });
        case "effort":
            return tasks.sort((a, b) => (a.effortEstimation || 0) - (b.effortEstimation || 0));
        default:
            return tasks;
    }
}

function displayTasks(tasks) {
    const tasksDL = document.querySelector("#tasks dl");
    const habitsDL = document.querySelector("#habits dl");

    tasksDL.innerHTML = "";
    habitsDL.innerHTML = "";

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    tasks.forEach(task => {
        const dueDate = task.dueDate ? new Date(task.dueDate) : null;
        if (dueDate) dueDate.setHours(0, 0, 0, 0);

        // ❌ Skip completed AND overdue tasks
        if (task.status === "Complete" && dueDate && dueDate < today) return;

        const dt = document.createElement("dt");
        const dd = document.createElement("dd");

        dt.style.backgroundColor = task.group_color || "#ffffff";
        dd.style.backgroundColor = task.group_color || "#ffffff";

        dt.textContent = task.taskName || "No title";

        const status = task.status || "Not Started";
        const priority = task.priority || 0;
        const effort = task.effortEstimation || 0;

        dd.innerHTML = `
            <span class="task-text">
                ${task.description || ""} — Due: ${task.dueDate || ""} |
                Status: ${status} | Priority: ${priority} | Effort: ${effort}
            </span>
        `;

        // ✅ Status logic
        if (status === "Complete") {
            dt.style.textDecoration = "line-through";
            dd.style.textDecoration = "line-through";
            dt.style.opacity = "0.6";
            dd.style.opacity = "0.6";
        } else if (dueDate && dueDate < today) {
            const warning = document.createElement("span");
            warning.textContent = " ⚠️ OVERDUE";
            warning.style.color = "red";
            warning.style.fontWeight = "bold";
            dt.appendChild(warning);
        }

        // Modify button
        const modifyBtn = document.createElement("button");
        modifyBtn.textContent = "Modify";
        modifyBtn.style.float = "right"; // right-align
        modifyBtn.addEventListener("click", () => {
            window.location.href = `/modify_task?taskID=${task.task_id}`;
        });
        dd.appendChild(modifyBtn);

        // Append to correct section
        if (task.habit) {
            habitsDL.appendChild(dt);
            habitsDL.appendChild(dd);
        } else {
            tasksDL.appendChild(dt);
            tasksDL.appendChild(dd);
        }
    });
}

// Filter menu setup
document.addEventListener("DOMContentLoaded", () => {
    const filterBtn = document.getElementById("filterBtn");
    const filterMenu = document.getElementById("filterMenu");

    if (filterBtn && filterMenu) {
        filterBtn.addEventListener("click", () => filterMenu.classList.toggle("hidden"));
        filterMenu.querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", () => {
                currentFilter = btn.dataset.filter || "none";
                filterMenu.classList.add("hidden");
                fetchTasks(); // re-fetch + apply filter
            });
        });
    }

    fetchTasks(); // initial load
});