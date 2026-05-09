# API Endpoints & Examples

Complete documentation of all REST API endpoints with examples.

## Base URL
```
http://localhost:5000/api
```

---

## 👥 PATIENT ENDPOINTS

### Get All Patients
**Endpoint:** `GET /api/patients/`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Alice Williams",
      "age": 32,
      "contact": "9876543210",
      "email": "alice@example.com",
      "address": "123 Main St",
      "created_at": "2026-05-05 10:30:00"
    }
  ],
  "count": 1
}
```

**cURL:**
```bash
curl http://localhost:5000/api/patients/
```

**JavaScript:**
```javascript
fetch('/api/patients/')
  .then(r => r.json())
  .then(d => console.log(d));
```

---

### Get Patient by ID
**Endpoint:** `GET /api/patients/<id>`

**Example:** `GET /api/patients/1`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice Williams",
    "age": 32,
    "contact": "9876543210",
    "email": "alice@example.com",
    "address": "123 Main St",
    "created_at": "2026-05-05 10:30:00"
  }
}
```

---

### Add Patient
**Endpoint:** `POST /api/patients/`

**Required Fields:** `name`, `age`, `contact`  
**Optional Fields:** `email`, `address`

**Request Body:**
```json
{
  "name": "John Doe",
  "age": 28,
  "contact": "9876543211",
  "email": "john@example.com",
  "address": "456 Oak Ave"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Patient added successfully",
  "data": {
    "id": 6,
    "name": "John Doe",
    "age": 28,
    "contact": "9876543211",
    "email": "john@example.com",
    "address": "456 Oak Ave",
    "created_at": "2026-05-05 14:20:00"
  }
}
```

**cURL:**
```bash
curl -X POST http://localhost:5000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 28,
    "contact": "9876543211",
    "email": "john@example.com"
  }'
```

**Python:**
```python
import requests

data = {
    'name': 'John Doe',
    'age': 28,
    'contact': '9876543211',
    'email': 'john@example.com'
}

response = requests.post('http://localhost:5000/api/patients/', json=data)
print(response.json())
```

---

### Update Patient
**Endpoint:** `PUT /api/patients/<id>`

**Example:** `PUT /api/patients/1`

**Request Body:**
```json
{
  "name": "Alice Smith",
  "age": 33,
  "email": "alice.smith@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Patient updated successfully",
  "data": { ... }
}
```

---

### Delete Patient
**Endpoint:** `DELETE /api/patients/<id>`

**Example:** `DELETE /api/patients/1`

**Response:**
```json
{
  "success": true,
  "message": "Patient deleted successfully"
}
```

**cURL:**
```bash
curl -X DELETE http://localhost:5000/api/patients/1
```

---

### Search Patients
**Endpoint:** `GET /api/patients/search?q=<query>`

**Example:** `GET /api/patients/search?q=Alice`

**Response:**
```json
{
  "success": true,
  "data": [ ... ],
  "count": 1
}
```

**JavaScript:**
```javascript
const query = 'Alice';
fetch(`/api/patients/search?q=${query}`)
  .then(r => r.json())
  .then(d => console.log(d));
```

---

## 👨‍⚕️ DOCTOR ENDPOINTS

### Get All Doctors
**Endpoint:** `GET /api/doctors/`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "John Smith",
      "specialization": "Cardiology",
      "contact": "9876543210",
      "email": "john.smith@clinic.com",
      "available_days": "Monday, Tuesday, Wednesday, Thursday, Friday",
      "start_time": "09:00",
      "end_time": "17:00",
      "created_at": "2026-05-05 10:30:00"
    }
  ],
  "count": 1
}
```

---

### Add Doctor
**Endpoint:** `POST /api/doctors/`

**Required Fields:** `name`, `specialization`, `contact`  
**Optional Fields:** `email`, `available_days`, `start_time`, `end_time`

**Request Body:**
```json
{
  "name": "Sarah Johnson",
  "specialization": "Neurology",
  "contact": "9876543220",
  "email": "sarah@clinic.com",
  "available_days": "Monday, Wednesday, Friday",
  "start_time": "10:00",
  "end_time": "18:00"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Doctor added successfully",
  "data": { ... }
}
```

---

### Get Doctors by Specialization
**Endpoint:** `GET /api/doctors/by-specialization/<specialization>`

**Example:** `GET /api/doctors/by-specialization/Cardiology`

**Response:**
```json
{
  "success": true,
  "data": [ ... ],
  "count": 2
}
```

---

## 📅 APPOINTMENT ENDPOINTS

### Get All Appointments
**Endpoint:** `GET /api/appointments/`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "patient_id": 1,
      "patient_name": "Alice Williams",
      "doctor_id": 1,
      "doctor_name": "John Smith",
      "doctor_specialization": "Cardiology",
      "appointment_date": "2026-05-07",
      "appointment_time": "10:00",
      "priority": "normal",
      "status": "scheduled",
      "reason": "Regular checkup",
      "notes": null,
      "created_at": "2026-05-05 10:30:00"
    }
  ],
  "count": 1
}
```

---

### Book Appointment
**Endpoint:** `POST /api/appointments/`

**Required Fields:** `patient_id`, `doctor_id`, `appointment_date`, `appointment_time`  
**Optional Fields:** `priority`, `reason`, `notes`

**Request Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 2,
  "appointment_date": "2026-05-15",
  "appointment_time": "14:00",
  "priority": "normal",
  "reason": "Follow-up consultation"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Appointment booked successfully",
  "data": { ... }
}
```

**Error Response (Double Booking):**
```json
{
  "success": false,
  "error": "This time slot is already booked"
}
```

**Python Example:**
```python
import requests
from datetime import datetime, timedelta

data = {
    'patient_id': 1,
    'doctor_id': 2,
    'appointment_date': '2026-05-15',
    'appointment_time': '14:00',
    'priority': 'normal',
    'reason': 'Checkup'
}

response = requests.post(
    'http://localhost:5000/api/appointments/',
    json=data
)

result = response.json()
if result['success']:
    print(f"Appointment ID: {result['data']['id']}")
else:
    print(f"Error: {result['error']}")
```

---

### Suggest Next Available Slot
**Endpoint:** `GET /api/appointments/suggest-slot/<doctor_id>`

**Optional Query Parameters:**
- `date`: Preferred date (YYYY-MM-DD format)

**Example:** `GET /api/appointments/suggest-slot/1?date=2026-05-10`

**Response:**
```json
{
  "success": true,
  "data": {
    "date": "2026-05-10",
    "time": "14:00",
    "day": "Saturday"
  }
}
```

**JavaScript:**
```javascript
const doctorId = 2;
const preferredDate = '2026-05-15';

fetch(`/api/appointments/suggest-slot/${doctorId}?date=${preferredDate}`)
  .then(r => r.json())
  .then(d => {
    if (d.success) {
      console.log(`Available: ${d.data.date} at ${d.data.time}`);
    }
  });
```

---

### Get Patient Appointments
**Endpoint:** `GET /api/appointments/patient/<patient_id>`

**Example:** `GET /api/appointments/patient/1`

**Response:**
```json
{
  "success": true,
  "data": [ ... ],
  "count": 3
}
```

---

### Get Doctor Appointments
**Endpoint:** `GET /api/appointments/doctor/<doctor_id>`

**Example:** `GET /api/appointments/doctor/2`

**Response:**
```json
{
  "success": true,
  "data": [ ... ],
  "count": 5
}
```

---

### Get Urgent Appointments
**Endpoint:** `GET /api/appointments/urgent-appointments`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 2,
      "patient_name": "Bob Miller",
      "doctor_name": "Michael Brown",
      "appointment_date": "2026-05-06",
      "appointment_time": "09:00",
      "priority": "urgent",
      "status": "scheduled"
    }
  ],
  "count": 1
}
```

---

### Update Appointment
**Endpoint:** `PUT /api/appointments/<id>`

**Example:** `PUT /api/appointments/1`

**Request Body:**
```json
{
  "priority": "urgent",
  "status": "completed",
  "notes": "Patient feeling better"
}
```

---

### Cancel Appointment
**Endpoint:** `DELETE /api/appointments/<id>`

**Example:** `DELETE /api/appointments/1`

**Response:**
```json
{
  "success": true,
  "message": "Appointment cancelled successfully"
}
```

---

## 🔧 SYSTEM ENDPOINTS

### Health Check
**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-05T14:30:00.123456",
  "service": "Smart Clinic Management System"
}
```

**Use Case:** Check if server is running
```bash
curl http://localhost:5000/api/health
```

---

### Get Statistics
**Endpoint:** `GET /api/stats`

**Response:**
```json
{
  "success": true,
  "data": {
    "total_patients": 5,
    "total_doctors": 4,
    "total_appointments": 8,
    "scheduled_appointments": 6,
    "urgent_appointments": 1
  }
}
```

**Use Case:** Display dashboard statistics

---

## 📊 Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Missing required fields: name, age, contact"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Patient not found"
}
```

### 500 Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## 🧪 Testing with Postman

1. **Import Collection**
   - Create new collection
   - Add requests for each endpoint

2. **Sample Request (Add Patient)**
   - Method: POST
   - URL: http://localhost:5000/api/patients/
   - Headers: Content-Type: application/json
   - Body: 
     ```json
     {
       "name": "Test Patient",
       "age": 25,
       "contact": "9999999999"
     }
     ```

3. **Run Tests**
   - Click Send
   - Verify response

---

## 💻 Complete Python Example

```python
import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:5000/api'

class ClinicAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_patients(self):
        response = requests.get(f'{self.base_url}/patients/')
        return response.json()
    
    def add_patient(self, name, age, contact, email='', address=''):
        data = {
            'name': name,
            'age': age,
            'contact': contact,
            'email': email,
            'address': address
        }
        response = requests.post(f'{self.base_url}/patients/', json=data)
        return response.json()
    
    def book_appointment(self, patient_id, doctor_id, date, time, priority='normal'):
        data = {
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_date': date,
            'appointment_time': time,
            'priority': priority
        }
        response = requests.post(f'{self.base_url}/appointments/', json=data)
        return response.json()
    
    def get_urgent_appointments(self):
        response = requests.get(f'{self.base_url}/appointments/urgent-appointments')
        return response.json()

# Usage
api = ClinicAPI(BASE_URL)

# Add patient
result = api.add_patient('Jane Doe', 30, '9999999999')
if result['success']:
    print(f"Patient added: {result['data']['id']}")

# Get all patients
patients = api.get_patients()
print(f"Total patients: {patients['count']}")

# Get urgent appointments
urgent = api.get_urgent_appointments()
print(f"Urgent cases: {urgent['count']}")
```

---

## 🚀 Using with cURL

```bash
# Get all patients
curl http://localhost:5000/api/patients/

# Add patient
curl -X POST http://localhost:5000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","age":25,"contact":"9999999999"}'

# Get statistics
curl http://localhost:5000/api/stats

# Get urgent appointments
curl http://localhost:5000/api/appointments/urgent-appointments
```

---

For more examples, check the README.md file.
