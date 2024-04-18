from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer

class MachineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine_data = {'machine_name': 'Test Machine', 'machine_serial_no': '12345'}

    def test_create_machine(self):
        response = self.client.post(reverse('machine-list'), self.machine_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Machine.objects.count(), 1)
        self.assertEqual(Machine.objects.get().machine_name, 'Test Machine')

    def test_get_machine_list(self):
        Machine.objects.create(machine_name='Machine 1', machine_serial_no='1001')
        Machine.objects.create(machine_name='Machine 2', machine_serial_no='1002')
        response = self.client.get(reverse('machine-list'))
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_machine_detail(self):
        machine = Machine.objects.create(machine_name='Machine 1', machine_serial_no='1001')
        response = self.client.get(reverse('machine-detail', kwargs={'pk': machine.id}))
        serializer = MachineSerializer(machine)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_machine(self):
        machine = Machine.objects.create(machine_name='Machine 1', machine_serial_no='1001')
        updated_data = {'machine_name': 'Updated Machine', 'machine_serial_no': '1002'}
        response = self.client.put(reverse('machine-detail', kwargs={'pk': machine.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        machine.refresh_from_db()
        self.assertEqual(machine.machine_name, 'Updated Machine')

    def test_delete_machine(self):
        machine = Machine.objects.create(machine_name='Machine 1', machine_serial_no='1001')
        response = self.client.delete(reverse('machine-detail', kwargs={'pk': machine.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Machine.objects.count(), 0)

class ProductionLogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine = Machine.objects.create(machine_name='Test Machine', machine_serial_no='12345')
        self.production_log_data = {
            'cycle_no': 'CN001',
            'unique_id': '123456',
            'material_name': 'Test Material',
            'machine': self.machine.id,
            'start_time': '2024-04-19T09:00:00Z',
            'end_time': '2024-04-19T10:00:00Z',
            'duration':'1.0'
        }

    def test_create_production_log(self):
        
        response = self.client.post(reverse('production-log-list'), self.production_log_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionLog.objects.count(), 1)
        self.assertEqual(ProductionLog.objects.get().cycle_no, 'CN001')

    def test_get_production_log_list(self):
        ProductionLog.objects.create(cycle_no='CN001', unique_id='123456', material_name='Material 1', machine=self.machine,
                                     start_time='2024-04-19T09:00:00Z', end_time='2024-04-19T10:00:00Z',duration="1.0")
        ProductionLog.objects.create(cycle_no='CN002', unique_id='123457', material_name='Material 2', machine=self.machine,
                                     start_time='2024-04-19T09:00:00Z', end_time='2024-04-19T10:00:00Z',duration='1.0')
        response = self.client.get(reverse('production-log-list'))
        production_logs = ProductionLog.objects.all()
        serializer = ProductionLogSerializer(production_logs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_production_log_detail(self):
        production_log = ProductionLog.objects.create(cycle_no='CN001', unique_id='123456', material_name='Test Material',
                                                      machine=self.machine, start_time='2024-04-19T09:00:00Z',
                                                      end_time='2024-04-19T10:00:00Z',duration='1.0')

        response = self.client.get(reverse('production-log-detail', kwargs={'pk': production_log.id}))
        serializer = ProductionLogSerializer(production_log)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_production_log(self):
        production_log = ProductionLog.objects.create(cycle_no='CN001', unique_id='123456', material_name='Test Material',
                                                      machine=self.machine, start_time='2024-04-19T09:00:00Z',
                                                      end_time='2024-04-19T10:00:00Z',duration='1.0')
        updated_data = {'cycle_no': 'CN002', 'unique_id': '123457'}
        response = self.client.patch(reverse('production-log-detail', kwargs={'pk': production_log.id}), updated_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        production_log.refresh_from_db()
        self.assertEqual(production_log.cycle_no, 'CN002')