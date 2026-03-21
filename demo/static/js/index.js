console.log("index.js loaded");

async function fetchTasks() {
    try {
        const response = await fetch("/tasks");
        if (!response.ok) throw new Error("Failed to fetch tasks");

        const tasks = await response.json();
        console.log("Tasks received:", tasks);

        displayTasks(tasks);

    } catch (err) {
        console.error("Fetch error:", err);
    }
}

function displayTasks(tasks) {
    const tasksDL = document.querySelector("#tasks dl");
    const habitsDL = document.querySelector("#habits dl");

    tasksDL.innerHTML = "";
    habitsDL.innerHTML = "";

    const today = new Date();
    today.setHours(0, 0, 0, 0); // normalize

    tasks.forEach(task => {
        const dueDate = task.dueDate ? new Date(task.dueDate) : null;
        if (dueDate) dueDate.setHours(0, 0, 0, 0); // normalize

        // ❌ SKIP: completed AND overdue
        if (
            task.status === "Complete" &&
            dueDate &&
            dueDate < today
        ) {
            return;
        }

        const dt = document.createElement("dt");
        const dd = document.createElement("dd");
        const spacer = document.createElement("spacer");

        dt.style.backgroundColor = task.group_color || "#ffffff";
        dd.style.backgroundColor = task.group_color || "#ffffff";

        // Base text
        dt.textContent = task.taskName || "No title";
        spacer.textContent = " ";

        const status = task.status || "Not Started";
        const priority = (task.priority !== null && task.priority !== undefined && task.priority !== "")
            ? task.priority
            : 0;
        const effort = (task.effortEstimation !== null && task.effortEstimation !== undefined && task.effortEstimation !== "")
            ? task.effortEstimation
            : 0;

        dd.textContent =
            (task.description || "") +
            " — Due: " + (task.dueDate || "") +
            " | Status: " + status +
            " | Priority: " + priority +
            " | Effort: " + effort;

        // =========================
        // STATUS LOGIC (FIXED)
        // =========================

        // ✅ Completed (only non-overdue reach here)
        if (task.status === "Complete") {
            dt.style.textDecoration = "line-through";
            dd.style.textDecoration = "line-through";
            dt.style.opacity = "0.6";
            dd.style.opacity = "0.6";
        }

        // ⚠️ Overdue (only if NOT complete)
        else if (
            dueDate &&
            dueDate < today
        ) {
            const warning = document.createElement("span");
            warning.textContent = " ⚠️ OVERDUE";
            warning.style.color = "red";
            warning.style.fontWeight = "bold";

            dt.appendChild(warning);
        }

        // =========================
        // MODIFY BUTTON
        // =========================
        const modifyBtn = document.createElement("button");
        modifyBtn.textContent = "Modify";
        modifyBtn.style.marginLeft = "10px";

        modifyBtn.addEventListener("click", () => {
            window.location.href = `/modify_task?taskID=${task.task_id}`;
        });

        dd.appendChild(modifyBtn);

        // =========================
        // APPEND TO CORRECT SECTION
        // =========================
        if (task.habit) {
            habitsDL.appendChild(dt);
            habitsDL.appendChild(dd);
        } else {
            tasksDL.appendChild(dt);
            tasksDL.appendChild(dd);
        }
    });
}
// Run on page load
fetchTasks();