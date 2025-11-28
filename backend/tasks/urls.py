# from django.urls import path
# from .views import analyze_tasks, home

# urlpatterns = [
#     path('', home, name='home'),
#     path('api/tasks/analyze/', analyze_tasks, name='analyze_tasks'),
# ]

from django.urls import path
from .views import analyze_tasks, get_saved_results, delete_task,top_suggestions

urlpatterns = [
    # path('', home, name='home'),
    path('api/tasks/analyze/', analyze_tasks),
    path('api/tasks/results/', get_saved_results),
    path('api/tasks/delete/<int:id>/', delete_task, name='delete-task'),
    path('suggest/', top_suggestions, name='top_suggestions'),  # NEW


]
