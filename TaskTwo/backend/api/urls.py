from django.urls import path
from .views import MachineListCreateView, MachineDetailView, ProductionLogListCreateView, ProductionLogDetailView

urlpatterns = [
    path('machines/', MachineListCreateView.as_view(), name='machine-list'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('production_logs/', ProductionLogListCreateView.as_view(), name='production-log-list'),
    path('production_logs/<int:pk>/', ProductionLogDetailView.as_view(), name='production-log-detail'),
]
from django.urls import path
from .views import MachineListCreateView, MachineDetailView, ProductionLogListCreateView, ProductionLogDetailView

urlpatterns = [
    path('machines/', MachineListCreateView.as_view(), name='machine-list'),
    path('machines/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('production_logs/', ProductionLogListCreateView.as_view(), name='production-log-list'),
    path('production_logs/<int:pk>/', ProductionLogDetailView.as_view(), name='production-log-detail'),
]
