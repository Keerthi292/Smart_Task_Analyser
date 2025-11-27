from datetime import datetime, date

def score_task_list(tasks):
    results = []
    today = date.today()

    for t in tasks:
        title = t.get("title", "Untitled Task")
        importance = int(t.get("importance", 5))
        hours = float(t.get("estimated_hours", 1))
        due = t.get("due_date", None)
        
        if due:
            try:
                due = datetime.strptime(due, "%Y-%m-%d").date()
            except:
                due = None

        # Urgency calculation
        if due:
            days_left = (due - today).days
            urgency_score = 1 if days_left <= 0 else 1 / (days_left + 1)
        else:
            urgency_score = 0.1  # missing due date → low urgency

        # Effort score (less hours = higher priority)
        effort_score = 1 / (hours + 1)

        # Final score (simple weighted average)
        score = round(((importance * 0.5) + (urgency_score * 0.3) + (effort_score * 0.2)), 3)

        results.append({
            "title": title,
            "importance": importance,
            "estimated_hours": hours,
            "due_date": t.get("due_date", None),
            "score": score,
        })

    # Sort highest priority first
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
