# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .scoring import score_task_list  # Your scoring logic

# @csrf_exempt
# def analyze_tasks(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST allowed"}, status=405)

#     try:
#         data = json.loads(request.body.decode("utf-8"))
#         tasks = data.get("tasks", [])
#     except:
#         return JsonResponse({"error": "Invalid JSON input"}, status=400)

#     results = score_task_list(tasks)  # Calculate scores
#     return JsonResponse({"results": results}, safe=False)

# def home(request):
#     return HttpResponse("<h1>Task Analyzer API is Running </h1>")

# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .scoring import score_task_list
# from .models import AnalyzedTask
# from django.shortcuts import get_object_or_404

# @csrf_exempt
# def analyze_tasks(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST allowed"}, status=405)

#     data = json.loads(request.body.decode('utf-8'))
#     tasks = data.get("tasks", [])
#     results = score_task_list(tasks)

#     saved_results = []
#     for r in results:
#         task = AnalyzedTask.objects.create(
#             title=r["title"],
#             importance=r["importance"],
#             estimated_hours=r["estimated_hours"],
#             due_date=r["due_date"] or None,
#             score=r["score"],
#             priority=r["priority"]
#         )
#         r["id"] = task.id
#         saved_results.append(r)

#     return JsonResponse({"results": saved_results})



# # Fetch saved results
# def get_saved_results(request):
#     saved = list(AnalyzedTask.objects.all().values())
#     return JsonResponse(saved, safe=False)



# @csrf_exempt
# def delete_task(request, id):
#     if request.method == "DELETE":
#         task = get_object_or_404(AnalyzedTask, id=id)  # Get the DB object
#         task.delete()                           # Delete from DB
#         return JsonResponse({"message": "Deleted"})
#     return JsonResponse({"error": "Invalid Method"}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import datetime

from .scoring import score_task_list
from .models import AnalyzedTask


@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    tasks = data.get("tasks", [])

    results = score_task_list(tasks)

    saved_results = []
    for r in results:
        obj = AnalyzedTask.objects.create(
            title=r["title"],
            importance=r["importance"],
            estimated_hours=r["estimated_hours"],
            due_date=r["due_date"] or None,
            score=r["score"],
            priority=r["priority"]
        )
        r["id"] = obj.id
        saved_results.append(r)

    return JsonResponse({"results": saved_results})


def get_saved_results(request):
    data = list(AnalyzedTask.objects.all().values())
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_task(request, id):
    if request.method == "DELETE":
        item = get_object_or_404(AnalyzedTask, id=id)
        item.delete()
        return JsonResponse({"message": "Deleted"})
    return JsonResponse({"error": "Invalid method"}, status=405)



def generate_explanation(task):
    explanation = []

    # Urgency
    if task.due_date:
        days_left = (task.due_date - datetime.date.today()).days
        if days_left < 0:
            explanation.append("Past due date")
        elif days_left <= 2:
            explanation.append("Very urgent")
        elif days_left <= 5:
            explanation.append("Medium urgency")
        else:
            explanation.append("Low urgency")
    else:
        explanation.append("No due date provided")

    # Importance
    if task.importance >= 8:
        explanation.append("Highly important")
    elif task.importance >= 5:
        explanation.append("Moderately important")
    else:
        explanation.append("Low importance")

    # Effort
    if task.estimated_hours <= 2:
        explanation.append("Low effort, quick to finish")
    elif task.estimated_hours <= 5:
        explanation.append("Medium effort")
    else:
        explanation.append("High effort task")

    return ", ".join(explanation)


def top_suggestions(request):

    tasks = AnalyzedTask.objects.all().order_by('-score')[:3]

    final = []

    for t in tasks:
        final.append({
            "id": t.id,
            "title": t.title,
            "importance": t.importance,
            "estimated_hours": t.estimated_hours,
            "due_date": str(t.due_date),
            "score": t.score,
            "priority": t.priority,
            "explanation": generate_explanation(t)
        })

    return JsonResponse({"top_tasks": final})



