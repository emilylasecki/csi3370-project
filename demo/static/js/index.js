console.log("JavaScript file is connected and running!");

document.addEventListener("DOMContentLoaded", function () {
    const tasks = JSON.parse(localStorage.getItem("tasks") || "[]");
    const dl = document.querySelector("#tasks dl");
 
    if (tasks)
    {
        tasks.forEach(function (task) {
            const dt = document.createElement("dt");
            // dt.textContent = task.taskTitle;
            dt.textContent = task.title;
    
            const dd = document.createElement("dd");
            dd.textContent = task.description
                + " — Due: " + task.dueDate 
                + " [" + task.status + "]" + ""
                + " [" + task.effort + "]" + ""
                + " [" + task.priority + "]";

    
            dl.appendChild(dt);
            dl.appendChild(dd);
        });
    }
});
 