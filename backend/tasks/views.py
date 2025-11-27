from django.shortcuts import render

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scoring import score_task_list
from django.http import HttpResponse


@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        tasks = data.get("tasks", [])
    except:
        return JsonResponse({"error": "Invalid JSON input"}, status=400)

    result = score_task_list(tasks)
    return JsonResponse({"results": result}, safe=False)

def home(request):
    return HttpResponse("<h1>Task Analyzer API is Running </h1>")