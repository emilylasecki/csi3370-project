console.log("JavaScript file is connected and running!");

document.querySelector("form[action='/add_task']").addEventListener("submit", function (e) {
    e.preventDefault();

    const taskTitle = document.getElementById("title").value;
    const taskDesc = document.getElementById("description").value;
    const taskStatus = document.getElementById("status").value;
    const taskDueDate = document.getElementById("due").value;
    const taskPriority = document.getElementById("priority").value;
    const taskEffort = document.getElementById("effort").value;

    console.log(taskTitle);
 
    if (!taskTitle || !taskDesc || !taskDueDate) return;
 
    // const tasks = JSON.parse(localStorage.getItem("tasks") || "[]");
    // tasks.push({ taskTitle, taskDesc, taskStatus, taskDueDate, taskPriority, taskEffort });
    // localStorage.setItem("tasks", JSON.stringify(tasks)); 

    saveTask({
      title: taskTitle,
      description: taskDesc,
      status: taskStatus,
      dueDate: taskDueDate,
      priority: taskPriority,
      effort: taskEffort
    });

    window.location.href = "/";

    function saveTask(task) { //Save locally
    const tasks = JSON.parse(localStorage.getItem("tasks") || "[]");
    tasks.push(task);
    localStorage.setItem("tasks", JSON.stringify(tasks));

    // fetch("/add_task_json", {
    //     method: "POST",
    //     headers: { "Content-Type": "application/json" },
    //     body: JSON.stringify(task)
    // })
    // .then(res => res.json())
    // .then(data => console.log("Saved to JSON:", data))
    // .catch(err => console.error(err))
    
    console.log("Saved task:", task);
    }

    // Hopefully, save to database
    // async function saveTask(task) {
    // const { data, error } = await supabase
    //     .from("tasks")
    //     .insert([task]);

    // if (error) console.error(error);
    // }
});

