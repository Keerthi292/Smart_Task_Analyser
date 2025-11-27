let tasks = [];

document.getElementById("addBtn").addEventListener("click", () => {
  const title = document.getElementById("title").value;
  const importance = document.getElementById("importance").value || 5;
  const hours = document.getElementById("hours").value || 1;
  const due = document.getElementById("due").value;

  if (!title) {
    alert("Task title is required");
    return;
  }

  tasks.push({
    title,
    importance,
    estimated_hours: hours,
    due_date: due
  });

  renderTasks();
  clearInputs();
});

function renderTasks() {
  const tbody = document.querySelector("#taskTable tbody");
  tbody.innerHTML = "";
  tasks.forEach(t => {
    tbody.innerHTML += `
      <tr>
        <td>${t.title}</td>
        <td>${t.importance}</td>
        <td>${t.estimated_hours}</td>
        <td>${t.due_date || "-"}</td>
      </tr>`;
  });
}

function clearInputs() {
  document.getElementById("title").value = "";
  document.getElementById("importance").value = "";
  document.getElementById("hours").value = "";
  document.getElementById("due").value = "";
}

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
  showResults(data.results);
});

function showResults(results) {
  const tbody = document.querySelector("#resultTable tbody");
  tbody.innerHTML = "";
  results.forEach(r => {
    tbody.innerHTML += `
      <tr>
        <td>${r.title}</td>
        <td><b>${r.score}</b></td>
        <td>${r.importance}</td>
        <td>${r.estimated_hours}</td>
        <td>${r.due_date || "-"}</td>
      </tr>`;
  });
}
