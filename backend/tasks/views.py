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

    data = json.loads(request.body.decode('utf-8'))
    tasks = data.get("tasks", [])
    results = score_task_list(tasks)

    saved_results = []
    for r in results:
        task = AnalyzedTask.objects.create(
            title=r["title"],
            importance=r["importance"],
            estimated_hours=r["estimated_hours"],
            due_date=r["due_date"] or None,
            score=r["score"],
            priority=r["priority"]
        )
        r["id"] = task.id
        saved_results.append(r)

    return JsonResponse({"results": saved_results})



# Fetch saved results
def get_saved_results(request):
    saved = list(AnalyzedTask.objects.all().values())
    return JsonResponse(saved, safe=False)



@csrf_exempt
def delete_task(request, id):
    if request.method == "DELETE":
        task = get_object_or_404(AnalyzedTask, id=id)  # Get the DB object
        task.delete()                           # Delete from DB
        return JsonResponse({"message": "Deleted"})
    return JsonResponse({"error": "Invalid Method"}, status=405)


