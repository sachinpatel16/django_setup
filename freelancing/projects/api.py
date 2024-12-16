from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated , AllowAny # Optional: Restrict access
from rest_framework.decorators import action
from rest_framework.response import Response

from celery.result import AsyncResult
from .models import Project, ProjectType
from .serializers import ProjectSerializer, ProjectCreateUpdateSerializer, ProjectTypeSerializer

from freelancing.utils.permissions import IsAPIKEYAuthenticated
from freelancing.projects.tasks import sum

class ProjectTypeViewSet(ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    # permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]  # Optional
    permission_classes = [AllowAny]
    
    @action(methods=['post'], detail=False, url_path="celery")
    def celery(self, request, *args, **kwargs):
        try:
            a = int(request.GET.get('a', 0))
            b = int(request.GET.get('b', 0))
        except ValueError:
            return Response({"error": "Invalid input. 'a' and 'b' must be integers."}, status=400)
        
        result = sum.delay(a, b)
        print(result)
        return Response({"task_id": result.id, "message": "Task submitted!"})
    
    @action(methods=['get'], detail=False, url_path="celery-result")
    def celery_result(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id', None)
        if not task_id:
            return Response({"error": "Missing 'task_id' in query params."}, status=400)
        
        # Retrieve the result using AsyncResult
        task_result = AsyncResult(task_id)
        if task_result.state == 'PENDING':
            return Response({"task_id": task_id, "state": task_result.state, "message": "Task is still processing."})
        elif task_result.state == 'FAILURE':
            return Response({"task_id": task_id, "state": task_result.state, "error": str(task_result.result)})
        else:
            return Response({"task_id": task_id, "state": task_result.state, "result": task_result.result})
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.select_related('type').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer

    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]  # Optional
