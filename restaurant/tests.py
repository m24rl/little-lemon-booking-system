import json
from django.test import TestCase
from .models import Booking

class BookingWorkflowTests(TestCase):
    def test_empty_date_and_filtered_bookings(self):
        Booking.objects.create(first_name='Ada', reservation_date='2030-01-01', reservation_slot=11)
        self.assertEqual(self.client.get('/bookings?date=2030-01-02').json(), [])
        data = self.client.get('/bookings?date=2030-01-01').json()
        self.assertEqual(data[0]['fields']['first_name'], 'Ada')
        self.assertEqual(len(self.client.get('/bookings').json()), 1)

    def test_duplicate_slot_cannot_be_booked(self):
        payload = {'first_name':'Ada', 'reservation_date':'2030-01-01', 'reservation_slot':10}
        self.assertEqual(self.client.post('/bookings', json.dumps(payload), content_type='application/json').status_code, 201)
        self.assertIn(self.client.post('/bookings', json.dumps(payload), content_type='application/json').status_code, [400,409])
        self.assertEqual(Booking.objects.count(), 1)
        payload['reservation_date'] = '2030-01-02'
        self.assertEqual(self.client.post('/bookings', json.dumps(payload), content_type='application/json').status_code, 201)

    def test_invalid_requests(self):
        self.assertEqual(self.client.post('/bookings', 'bad json', content_type='application/json').status_code, 400)
        self.assertEqual(self.client.get('/bookings?date=2030-02-31').status_code, 400)
        payload = {'first_name':'Ada', 'reservation_date':'2030-01-01', 'reservation_slot':30}
        self.assertEqual(self.client.post('/bookings', json.dumps(payload), content_type='application/json').status_code, 400)
        self.assertEqual(Booking.objects.count(), 0)

    def test_reservations_renders_safe_json_and_form(self):
        Booking.objects.create(first_name='<script>alert(1)</script>', reservation_date='2030-01-01', reservation_slot=11)
        response = self.client.get('/reservations/')
        self.assertContains(response, 'reservation-data')
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(self.client.get('/book/'), 'type="date"')
