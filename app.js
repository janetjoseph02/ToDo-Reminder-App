document.getElementById("add-task-btn").addEventListener("click", () => {
    const taskInput = document.getElementById("task-input");
    const task = taskInput.value.trim();
    if (task) {
        fetch("/api/todos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ task, completed: false }),
        }).then(() => {
            taskInput.value = "";
            loadTasks();
        });
    }
});

function loadTasks() {
    fetch("/api/todos")
        .then((response) => response.json())
        .then((tasks) => {
            const todoList = document.getElementById("todo-list");
            todoList.innerHTML = "";
            tasks.forEach((task) => {
                const li = document.createElement("li");
                li.className = "task";
                li.innerHTML = `
                    <span>${task.task}</span>
                    <button onclick="deleteTask('${task._id}')">Delete</button>
                `;
                todoList.appendChild(li);
            });
        });
}

function deleteTask(taskId) {
    fetch(`/api/todos/${taskId}`, { method: "DELETE" }).then(() => {
        loadTasks();
    });
}

loadTasks();
