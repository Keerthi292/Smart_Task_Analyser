let tasks = [];       // User-added tasks
let resultsData = []; // Analyzed results

// Add task
document.getElementById("addBtn").addEventListener("click", () => {
  const title = document.getElementById("title").value;
  const importance = document.getElementById("importance").value || 5;
  const hours = document.getElementById("hours").value || 1;
  const due = document.getElementById("due").value;

  if (!title) {
    alert("Task title is required");
    return;
  }

  tasks.push({ title, importance, estimated_hours: hours, due_date: due });
  renderTasks();
  clearInputs();
});

// Render task list table
function renderTasks() {
  const tbody = document.querySelector("#taskTable tbody");
  tbody.innerHTML = "";
  tasks.forEach(t => {
    tbody.innerHTML += `<tr>
        <td>${t.title}</td>
        <td>${t.importance}</td>
        <td>${t.estimated_hours}</td>
        <td>${t.due_date || "-"}</td>
      </tr>`;
  });
}

// Clear inputs
function clearInputs() {
  document.getElementById("title").value = "";
  document.getElementById("importance").value = "";
  document.getElementById("hours").value = "";
  document.getElementById("due").value = "";
}

// Analyze tasks
document.getElementById("analyzeBtn").addEventListener("click", async () => {
  if (tasks.length === 0) {
    alert("Please add at least one task.");
    return;
  }

  const response = await fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tasks })
  });

  const data = await response.json();
  resultsData = data.results; // store analysis results separately
  renderResults();            // display in results table
});

function renderResults() {
  const tbody = document.querySelector("#resultTable tbody");
  tbody.innerHTML = "";

  resultsData.forEach(r => {
    let urgency = r.priority || "";
    let color = "";

    if (urgency === "High Urgency") color = "#ff4d4f";
    else if (urgency === "Medium Urgency") color = "#faad14";
    else color = "#52c41a";

    tbody.innerHTML += `<tr>
        <td>${r.title}</td>
        <td><b>${parseFloat(r.score).toFixed(2)}</b></td>
        <td>${r.importance}</td>
        <td>${r.estimated_hours}</td>
        <td>${r.due_date || "-"}</td>
        <td style="color:${color}; font-weight:bold">${urgency}</td>
        <td><button onclick="deleteResult('${r.id}')">
            Delete</button></td>
      </tr>`;
  });
}


// Fetch saved priority results on page load
window.onload = async () => {
  const response = await fetch("http://127.0.0.1:8000/api/tasks/results/");
  const data = await response.json();
  if (data.length > 0) {
    resultsData = data;
    renderResults();
  }
};
async function deleteResult(id) {
  if (!confirm("Are you sure you want to delete this task?")) return;

  await fetch(`http://127.0.0.1:8000/api/tasks/delete/${id}/`, {
    method: "DELETE"
  });

  // reload list
  resultsData = resultsData.filter(r => r.id != id);
  renderResults();
}

