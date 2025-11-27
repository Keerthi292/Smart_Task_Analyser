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
#     return HttpResponse("<h1>Task Analyzer API is Running 🚀</h1>")
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .scoring import score_task_list
from .models import AnalyzedTask
from django.shortcuts import get_object_or_404

@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        tasks = data.get("tasks", [])
    except:
        return JsonResponse({"error": "Invalid JSON input"}, status=400)

    results = score_task_list(tasks)

    # save new results (append)
    for r in results:
        if r["score"] >= 8:
            priority = "High Urgency"
        elif r["score"] >= 5:
            priority = "Medium Urgency"
        else:
            priority = "Low Urgency"

        AnalyzedTask.objects.create(
            title=r["title"],
            importance=r["importance"],
            estimated_hours=r["estimated_hours"],
            due_date=r["due_date"] or None,
            score=r["score"],
            priority=priority
        )

    return JsonResponse({"results": results}, safe=False)


# Fetch saved results
def get_saved_results(request):
    saved = list(AnalyzedTask.objects.all().values())
    return JsonResponse(saved, safe=False)



@csrf_exempt
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return JsonResponse({"message": "Deleted"})

def home(request):
    return HttpResponse("<h1>Task Analyzer API is Running 🚀</h1>")

