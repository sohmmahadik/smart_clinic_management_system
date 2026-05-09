# Getting Started - Quick Start Guide

## ⚡ Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```

Then open your browser: **http://localhost:5000**

### 3. Or Run the CLI Version
```bash
python cli.py
```

That's it! You're ready to use the system.

---

## 🌐 Web Interface (Recommended)

### Start the Server
```bash
python app.py
```

Output:
```
============================================================
Smart Clinic Management System
============================================================
Starting server on http://localhost:5000
Press Ctrl+C to stop the server
============================================================
```

### Access the System
- **Home**: http://localhost:5000/
- **Dashboard**: http://localhost:5000/dashboard
- **Patients**: http://localhost:5000/patients
- **Doctors**: http://localhost:5000/doctors
- **Appointments**: http://localhost:5000/appointments

### Features Available:
✅ Add/View/Edit/Delete Patients  
✅ Add/View/Edit/Delete Doctors  
✅ Book/View/Cancel Appointments  
✅ Search functionality  
✅ Statistics & Dashboard  
✅ Smart appointment scheduling  
✅ Conflict prevention  

---

## 💻 CLI Interface (Alternative)

### Start the CLI Program
```bash
python cli.py
```

### Main Menu
```
Main Menu:
========================================================
1. Patient Management
2. Doctor Management
3. Appointment Management
4. View Dashboard
5. Exit
```

### Operations:
- **Patient Management**: Add, View, Search, Update, Delete
- **Doctor Management**: Add, View, Search, Update, Delete
- **Appointment Management**: Book, View, Cancel, Suggest Slots
- **Dashboard**: View statistics

---

## 🎓 Sample Usage

### Via Web Interface:

1. **Add a Patient**
   - Click "Patients" → "Add Patient"
   - Fill in: Name, Age, Contact, Email, Address
   - Click "Add Patient"

2. **Add a Doctor**
   - Click "Doctors" → "Add Doctor"
   - Fill in: Name, Specialization, Contact, Hours
   - Click "Add Doctor"

3. **Book an Appointment**
   - Click "Appointments" → "Book Appointment"
   - Select Patient and Doctor
   - Choose Date and Time
   - Click "Suggest Slot" for auto-suggestion
   - Click "Book Appointment"

### Via CLI Interface:

```
Main Menu:
1 ← Enter to access Patients

Patient Management:
1 ← Enter to Add Patient

Patient Full Name: John Doe
Age: 30
Contact Number: 9876543210
Email: john@example.com
Address: 123 Main St

✅ Patient added successfully! (ID: 1)
```

---

## 🐛 Troubleshooting

### "Port 5000 already in use"
```bash
# Change port in app.py, line 71:
app.run(debug=True, host='localhost', port=5001)  # Changed from 5000 to 5001
```

### "ModuleNotFoundError"
```bash
# Install dependencies:
pip install -r requirements.txt

# Or individually:
pip install flask flask-cors flask-sqlalchemy
```

### "Permission denied" (Mac/Linux)
```bash
# Make app executable:
chmod +x app.py cli.py
```

### Reset Database
```bash
# Delete the database file:
rm clinic.db
# or on Windows:
del clinic.db

# Restart app to recreate:
python app.py
```

---

## 📱 API Testing

### Using curl (Command Line)
```bash
# Get all patients
curl http://localhost:5000/api/patients/

# Get all doctors
curl http://localhost:5000/api/doctors/

# Get statistics
curl http://localhost:5000/api/stats

# Get health status
curl http://localhost:5000/api/health
```

### Using Python
```python
import requests

# Get all patients
response = requests.get('http://localhost:5000/api/patients/')
print(response.json())

# Get all doctors
response = requests.get('http://localhost:5000/api/doctors/')
print(response.json())
```

### Using JavaScript (Browser Console)
```javascript
// Get all patients
fetch('/api/patients/')
    .then(r => r.json())
    .then(d => console.log(d));

// Get statistics
fetch('/api/stats')
    .then(r => r.json())
    .then(d => console.log(d));
```

---

## 🗂️ File Structure

```
Smart Clinic Management System/
├── app.py                 ← Main Flask app (RUN THIS for web)
├── cli.py                 ← CLI version (RUN THIS for command-line)
├── requirements.txt       ← Python packages to install
├── clinic.db             ← Database (auto-created)
├── README.md             ← Full documentation
├── GETTING_STARTED.md    ← This file
├── models/
│   ├── models.py         ← Database models
│   └── utils.py          ← Business logic
├── routes/
│   ├── patients.py       ← Patient endpoints
│   ├── doctors.py        ← Doctor endpoints
│   └── appointments.py   ← Appointment endpoints
├── templates/            ← HTML pages
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── patients.html
│   ├── doctors.html
│   └── appointments.html
└── static/
    └── style.css         ← Styling
```

---

## 💡 Tips & Tricks

### 1. Use Sample Data
First run automatically loads sample patients, doctors, and appointments.

### 2. Search Functionality
- Patients: Search by name or contact number
- Doctors: Search by name or specialization

### 3. Appointment Smart Features
- "Suggest Slot" automatically finds next available time
- Double-booking is prevented automatically
- Past dates cannot be selected
- Only working hours are allowed

### 4. Priority System
- **Normal**: Regular appointments
- **Urgent**: Priority cases (visible in dashboard)

### 5. Doctor Availability
- Set available days (e.g., "Monday, Wednesday, Friday")
- Set working hours (e.g., "09:00" to "17:00")
- System prevents bookings outside these times

---

## 🔗 Common API Endpoints

```
# Patients
GET    /api/patients/              - List all
GET    /api/patients/<id>          - Get one
POST   /api/patients/              - Create
PUT    /api/patients/<id>          - Update
DELETE /api/patients/<id>          - Delete
GET    /api/patients/search?q=...  - Search

# Doctors
GET    /api/doctors/               - List all
POST   /api/doctors/               - Create
GET    /api/doctors/by-specialization/<spec> - Filter

# Appointments
GET    /api/appointments/          - List all
POST   /api/appointments/          - Book
GET    /api/appointments/suggest-slot/<id> - Find slot
GET    /api/appointments/urgent-appointments - Urgent only

# System
GET    /api/health                 - Status check
GET    /api/stats                  - Statistics
```

---

## 🎯 Next Steps

1. **Explore the System**
   - Add some sample data
   - Try booking appointments
   - Test the search features

2. **Integrate with Your System**
   - Use the REST API for integration
   - Check API endpoints documentation

3. **Customize**
   - Modify templates in `templates/`
   - Update styles in `static/style.css`
   - Extend models in `models/models.py`

4. **Deploy**
   - Use Gunicorn for production: `pip install gunicorn`
   - Run: `gunicorn -w 4 app:app`
   - Add a reverse proxy (Nginx)

---

## 📞 Support

For detailed documentation, see **README.md**

Common issues:
- Check port availability
- Verify Python version (3.8+)
- Ensure all dependencies installed
- Clear browser cache if UI doesn't load

---

## 🚀 You're All Set!

**Web Interface**: `python app.py` → http://localhost:5000  
**CLI Version**: `python cli.py`  

Enjoy using the Smart Clinic Management System! 🏥
