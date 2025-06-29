const API_URL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
    fetchTodos();
    fetchStats();

    document.getElementById("todo-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
    
        await fetch(`${API_URL}/todos/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });
    
        document.getElementById("todo-form").reset();
        fetchTodos();
        fetchStats();
    });
});

async function fetchTodos() {
    const res = await fetch(`${API_URL}/todos/`);
    const todos = await res.json();
    const table = document.getElementById("todo-table");
    table.innerHTML = "";
    todos.forEach(todo => {
        table.innerHTML += `
        <tr>
        <td>${todo.title}</td>
        <td>${todo.description || ""}</td>
        <td class="text-capitalize text-center">${todo.status}</td>
        <td class="text-center">${todo.created_at ? new Date(todo.created_at).toLocaleString() : "-"}</td>
        <td class="text-center">${todo.completed_at ? new Date(todo.completed_at).toLocaleString() : '-'}</td>
        <td class="text-center">
            <button class="btn btn-success btn-sm" onclick="updateStatus(${todo.id}, 'completed')">✔</button>
            <button class="btn btn-warning btn-sm" onclick="updateStatus(${todo.id}, 'cancelled')">✖</button>
            <button class="btn btn-danger btn-sm" onclick="deleteTodo(${todo.id})">🗑</button>
        </td>
        </tr>
    `;
    });
}

async function updateStatus(id, status) {
    await fetch(`${API_URL}/todos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status })
    });
    fetchTodos();
    fetchStats();
}

async function deleteTodo(id) {
    await fetch(`${API_URL}/todos/${id}`, { method: "DELETE" });
    fetchTodos();
    fetchStats();
}

async function fetchStats() {
    const res = await fetch(`${API_URL}/todos/stats`);
    const stats = await res.json();
    document.getElementById("completed-count").textContent = stats.completed;
    document.getElementById("pending-count").textContent = stats.pending;
    document.getElementById("cancelled-count").textContent = stats.cancelled;
    document.getElementById("avg-time").textContent = `${stats.avg_time} min`;

    const ctx = document.getElementById("productivityChart").getContext("2d");
    if (window.productivityChart && typeof window.productivityChart.destroy == 'function') {
        window.productivityChart.destroy();
    }
    window.productivityChart = new Chart(ctx, {
        type: "doghnut",
        data: {
            labels: ["Completed", "Pending", "Cancelled"],
            datasets: [{
                label: "Todos",
                data: [stats.completed, stats.pending, stats.cancelled],
                backgroundColor: ["#198754", "#ffc107", "#dc3545"],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: {
                animateScale: true,
                animateRotate: true,
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            console.log(context);
                            const total = context.chart._metasets[0].total;
                            const value = context.raw;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ${value} (${percentage}%)`;
                        }
                    }
                },
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", fetchStats);
    