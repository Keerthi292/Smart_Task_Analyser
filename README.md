# Smart_Task_Analyser
Smart Task Analyzer is a simple AI-assisted task management tool that helps users decide which tasks they should do first based on urgency, importance, time required, and due date.

# Features

 Add tasks with title, importance, estimated hours, and due date
 Analyze all tasks using a Django REST API
 Automatically calculates score based on urgency & importance
 Shows Top 3 most important tasks
 Saves analyzed tasks in the database
 Delete tasks both from the frontend and the backend
 Clean UI built using HTML, CSS, and JavaScript

 # How it Works
 Frontend (HTML, CSS, JavaScript)
 * User enters tasks.
 * Tasks are sent to the Django backend through a POST API.
 * Results are displayed in a table along with priority levels.
 * A “Top 3 Suggestions” button fetches the top priority recommendations.
 * Delete button removes tasks from the database using a DELETE API.

 Backend (Django + Django REST Framework)
 * Receives task data from frontend.
 * Calculates a priority score using:
   .Task importance
   .Estimated time
   .Due date (closer date = higher urgency)
 * Saves analyzed tasks in the database.
 * Sends back sorted results with priority labels.
 * Provides an API to fetch the Top 3 tasks.

 # Technologies used 
 Frontend:
 HTML
 CSS
 JavaScript (Fetch API)
 
 Backend:
 Python
 Django
 Django REST Framework
 SQLite ( default database)

# API Endpoints
1) POST /api/tasks/analyze/   (Analyze Tasks)
2) GET /api/tasks/results/    (Fetch Saved Results)
3) DELETE /api/tasks/delete/<id>/  (Delete a Task)
4) GET /api/tasks/suggest/     (Get Top 3 Suggestions)

# How to Run the Project
 Backend Setup:
   pip install django 

<!-- create project -->
   django-admin startproject taskanalyser .

<!-- run project -->
   python manage.py runserver

 <!-- create django app -->
    python manage.py startapp tasks

  <!--migrate database  -->
   python manage.py makemigrations
   python manage.py migrate
   
 Frontend Setup:
  start index.html

# Algorithm exaplaination

The Smart Task Analyzer assigns a priority score to each task using three main factors: importance, urgency, and effort. These factors are combined into a single score that determines which tasks should be prioritise first. 
Step by step Workings:
1) Collect task details:
   * For each task, the algorithm reads:
   * Title – If missing, it defaults to "Untitled Task".
   * Importance – A number from 1 to 10 provided by the user; if missing, it defaults to 5.
   * Estimated Hours – How long the task will take; defaults to 1 hour if not provided.
   * Due Date – (optional; if missing, it’s handled later)

2) Calculate Urgency
   * If the task has a valid due date, it calculates how many days are left until the due date.
   * Overdue or due today: gets the highest urgency score (1)
   * Future due date: urgency decreases as the due date is further away. The formula used is 1 / (days_left + 1).
   * No due date: assigned a small urgency score (0.1) so it doesn’t get high priority.

3) Calculate Effort Score
   * Tasks that require less time are considered quicker wins.
   * Effort score is calculated as 1 / (hours + 1).

4) Combine Scores into Final Score
   * Each task gets a final priority score using a weighted sum:
   * final_score = (importance * 0.5) + (urgency_score * 0.3) + (effort_score * 0.2)
   * Importance contributes 50% of the score.
   * Urgency contributes 30% of the score.
   * Effort contributes 20% of the score.

5) Sort Tasks by Priority
   * After calculating scores, tasks are sorted in descending order so the highest-scoring tasks appear first.
   * These are the tasks the user should focus on immediately.

# Design Decisions
Why Django + SQLite:
  We used Django with SQLite because it’s lightweight and easy to set up for a small project. It handles database operations smoothly without extra configuration.

Why save analyzed tasks:
  Saving the analyzed tasks lets the results stay visible even after refreshing the page, so users don’t lose their data.

Why separate Top 3 suggestions:
  Showing the top 3 tasks separately gives users a quick, actionable list of what to do first without cluttering the main task list.

Frontend Decisions:
  Used plain HTML/CSS/JS for simplicity.
  Color-coded priority for better visualization. 
  Buttons for analyze, delete, and top suggestions to improve interactivity.

  Trade-offs:
   - Did not implement task dependencies to keep the project within the time limit.
   - Did not include login or multi-user support.

# Time Breakdown

Backend & API Development: 2.5 hours
Task model, scoring algorithm, CRUD APIs, Top 3 suggestions

Frontend Development: 1.5 hours
Task input form, results table, buttons, event handling, and styling

Testing & Debugging: 30–45 minutes
Fixing priority scoring, deletion, top suggestions, and API integration

# Future Improvements
  * Integrate user accounts for personal task management.
  * Make the frontend fully responsive for mobile devices.
  * Improve scoring algorithm using machine learning to learn user behavior.
  * Add task dependencies to make prioritization smarter.