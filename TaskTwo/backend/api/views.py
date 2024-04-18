from rest_framework import generics
from rest_framework.response import Response
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer

# List and Create operations for Machine
class MachineListCreateView(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

# Retrieve, Update, and Delete operations for Machine
class MachineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

# List and Create operations for ProductionLog
class ProductionLogListCreateView(generics.ListCreateAPIView):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer

# Retrieve, Update, and Delete operations for ProductionLog
class ProductionLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer
