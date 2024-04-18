from datetime import timedelta
from django.db import models


class Machine(models.Model):
    machine_name = models.CharField(max_length=255)
    machine_serial_no = models.CharField(max_length=255, unique=True)
    time = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.machine_name} ({self.machine_serial_no})"




class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100, unique=True)
    material_name = models.CharField(max_length=255)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='production_logs')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DecimalField(max_digits=5, decimal_places=2)  

    def __str__(self):
        return f"{self.cycle_no} - {self.unique_id}"

    