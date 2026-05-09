# Quick Reference Card

## 🚀 START HERE (Choose One)

### Web Interface (Recommended)
```bash
python app.py
# Then open: http://localhost:5000
```

### CLI Interface
```bash
python cli.py
```

### Easy Launcher
```bash
# Windows: Double-click run.bat
# Mac/Linux: chmod +x run.sh && ./run.sh
```

---

## 📋 ESSENTIAL COMMANDS

### Installation
```bash
pip install -r requirements.txt
```

### Run Web App
```bash
python app.py
```

### Run CLI
```bash
python cli.py
```

### Reset Database
```bash
# Delete clinic.db file, then restart app
rm clinic.db
python app.py
```

---

## 🌐 WEB URLS

| Feature | URL |
|---------|-----|
| Home | http://localhost:5000/ |
| Dashboard | http://localhost:5000/dashboard |
| Patients | http://localhost:5000/patients |
| Doctors | http://localhost:5000/doctors |
| Appointments | http://localhost:5000/appointments |

---

## 🔌 API QUICK ENDPOINTS

```bash
# Get all patients
curl http://localhost:5000/api/patients/

# Get all doctors
curl http://localhost:5000/api/doctors/

# Get statistics
curl http://localhost:5000/api/stats

# Get urgent appointments
curl http://localhost:5000/api/appointments/urgent-appointments
```

---

## 📊 KEY FEATURES

✅ **Patient Management**
- Add/Edit/Delete/Search patients
- Track contact & medical info

✅ **Doctor Management**
- Add/Edit/Delete doctors
- Set availability & specialization

✅ **Appointment System**
- Book appointments
- Prevent double-booking
- Suggest next slot
- Mark priority levels

✅ **Smart Features**
- Auto slot suggestion
- Double booking prevention
- Urgent case tracking
- Real-time statistics

---

## 📁 PROJECT STRUCTURE

```
Smart Clinic Management System/
├── app.py              ← RUN THIS for web
├── cli.py              ← RUN THIS for CLI
├── models/             ← Database models
├── routes/             ← API endpoints
├── templates/          ← HTML pages
├── static/             ← CSS styling
├── requirements.txt    ← Dependencies
└── clinic.db          ← Database (auto-created)
```

---

## 🔑 DATABASE MODELS

### Patients
```
id, name, age, contact, email, address, created_at
```

### Doctors
```
id, name, specialization, contact, email, 
available_days, start_time, end_time, created_at
```

### Appointments
```
id, patient_id, doctor_id, appointment_date, 
appointment_time, priority, status, reason, notes, created_at
```

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Port 5000 in use | Edit app.py, change port |
| Module error | `pip install -r requirements.txt` |
| Database error | Delete clinic.db, restart |
| CSS not loading | Clear browser cache (Ctrl+Shift+Delete) |
| Can't find app.py | Check you're in project directory |

---

## 📚 DOCUMENTATION FILES

- **README.md** - Full documentation (read this!)
- **GETTING_STARTED.md** - Quick start guide
- **API_ENDPOINTS.md** - All API endpoints with examples
- **PROJECT_SUMMARY.md** - Complete project overview

---

## ⚙️ SAMPLE DATA

**Pre-loaded on first run:**
- 5 Patients (Alice, Bob, Carol, David, Eve)
- 4 Doctors (Smith, Johnson, Brown, Davis)
- 5 Appointments (various dates/priorities)

Delete clinic.db to reset and reload sample data.

---

## 🎯 COMMON TASKS

### Add Patient (Web)
1. Click "Patients"
2. Click "Add Patient"
3. Fill form
4. Click "Add Patient"

### Add Doctor (Web)
1. Click "Doctors"
2. Click "Add Doctor"
3. Fill form & set hours
4. Click "Add Doctor"

### Book Appointment (Web)
1. Click "Appointments"
2. Click "Book Appointment"
3. Select patient & doctor
4. Choose date & time
5. Click "Suggest Slot" (optional)
6. Click "Book Appointment"

### Search Patient (Web)
1. Click "Patients"
2. Enter name/contact in search box
3. Click "Search"

---

## 🔗 IMPORTANT ENDPOINTS

### Patient API
```
GET    /api/patients/
POST   /api/patients/
GET    /api/patients/<id>
PUT    /api/patients/<id>
DELETE /api/patients/<id>
GET    /api/patients/search?q=name
```

### Doctor API
```
GET    /api/doctors/
POST   /api/doctors/
GET    /api/doctors/<id>
GET    /api/doctors/by-specialization/cardiology
```

### Appointment API
```
GET    /api/appointments/
POST   /api/appointments/
GET    /api/appointments/patient/<id>
GET    /api/appointments/doctor/<id>
GET    /api/appointments/suggest-slot/<id>
GET    /api/appointments/urgent-appointments
```

### System
```
GET    /api/health
GET    /api/stats
```

---

## 💻 PYTHON API EXAMPLE

```python
import requests

# Get all patients
r = requests.get('http://localhost:5000/api/patients/')
print(r.json())

# Add patient
data = {
    'name': 'John Doe',
    'age': 30,
    'contact': '9999999999'
}
r = requests.post('http://localhost:5000/api/patients/', json=data)
print(r.json())
```

---

## 📱 FEATURES AT A GLANCE

| Feature | Web | CLI |
|---------|-----|-----|
| Add Patient | ✅ | ✅ |
| View Patients | ✅ | ✅ |
| Search Patient | ✅ | ✅ |
| Edit Patient | ✅ | ✅ |
| Delete Patient | ✅ | ✅ |
| Add Doctor | ✅ | ✅ |
| View Doctors | ✅ | ✅ |
| Search Doctor | ✅ | ✅ |
| Book Appointment | ✅ | ✅ |
| View Appointments | ✅ | ✅ |
| Suggest Slot | ✅ | ✅ |
| Urgent Cases | ✅ | ✅ |
| Statistics | ✅ | ✅ |

---

## 🎓 REQUIREMENTS

- Python 3.8 or higher
- pip (Python package manager)
- Any modern web browser
- ~50MB disk space

---

## 📞 SUPPORT

1. Check **GETTING_STARTED.md** for common questions
2. Review **API_ENDPOINTS.md** for API details
3. Read **README.md** for comprehensive guide
4. Check inline code comments for implementation details

---

## ✨ TIPS & TRICKS

1. **Use "Suggest Slot"** - Automatically find next available time
2. **Set Working Hours** - Prevents invalid bookings
3. **Mark Urgent** - Highlight priority cases on dashboard
4. **Search First** - Find existing records before adding
5. **View Dashboard** - See real-time statistics
6. **Check Past Data** - All records have timestamps

---

## 🔄 WORKFLOW EXAMPLE

```
1. Add 2-3 Doctors (with hours)
   ↓
2. Add 5-10 Patients
   ↓
3. Book Appointments
   ↓
4. Use Suggest Slot for conflicts
   ↓
5. View Dashboard
   ↓
6. Manage appointments
```

---

## ⚡ PERFORMANCE TIPS

- Close unused browser tabs
- Use search for large lists
- Reset database if too many records
- Consider PostgreSQL for 10k+ records
- Use Gunicorn for production

---

## 🚀 DEPLOYMENT BASICS

### Local
```bash
python app.py
```

### Production
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

### Docker (optional)
```bash
docker build -t clinic .
docker run -p 5000:5000 clinic
```

---

## 🎯 PROJECT STATS

- **2000+** lines of Python code
- **1000+** lines of HTML/CSS/JS
- **25+** API endpoints
- **50+** functions
- **3** database models
- **0** external dependencies (except Flask)

---

**Quick Reference v1.0** | Built for Smart Clinic Management System

*For detailed info, see README.md*
