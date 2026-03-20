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

    if (!tasksDL || !habitsDL) {
        console.error("Missing #tasks or #habits container");
        return;
    }

    tasksDL.innerHTML = "";
    habitsDL.innerHTML = "";

    tasks.forEach(task => {
        const dt = document.createElement("dt");
        dt.textContent = task.taskName || "No title";
        dt.style.backgroundColor = task.group_color || "#ffffff";

        const dd = document.createElement("dd");
        dd.textContent =
            (task.description || "") +
            " — Due: " + (task.dueDate || "") +
            " [" + (task.status || "") + "]" +
            " [" + (task.effortEstimation || "") + "]" +
            " [" + (task.priority || "") + "]";
        dd.style.backgroundColor = task.group_color || "#ffffff";

        const modifyBtn = document.createElement("button");
        modifyBtn.textContent = "Modify";
        modifyBtn.style.marginLeft = "10px";

        modifyBtn.addEventListener("click", () => {
    // Redirect to modify page with taskID
    window.location.href = `/modify_task?taskID=${task.task_id}`;
});

        dd.appendChild(modifyBtn);

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