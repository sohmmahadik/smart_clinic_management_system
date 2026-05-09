"""
Smart Clinic Management System - Main Flask Application
A complete system to manage patients, doctors, and appointments
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from models import db
from routes import patient_bp, doctor_bp, appointment_bp
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialize database
db.init_app(app)

# Enable CORS for API
CORS(app)

# Register blueprints (API routes)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)


# Create app context and initialize database
with app.app_context():
    db.create_all()


# ============== HOME PAGE ROUTES ==============

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/patients')
def patients_page():
    """Patients management page"""
    return render_template('patients.html')


@app.route('/doctors')
def doctors_page():
    """Doctors management page"""
    return render_template('doctors.html')


@app.route('/appointments')
def appointments_page():
    """Appointments management page"""
    return render_template('appointments.html')


# ============== HEALTH CHECK & INFO ROUTES ==============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Smart Clinic Management System'
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get clinic statistics"""
    from models import Patient, Doctor, Appointment
    
    try:
        total_patients = Patient.query.count()
        total_doctors = Doctor.query.count()
        total_appointments = Appointment.query.count()
        scheduled_appointments = Appointment.query.filter_by(status='scheduled').count()
        urgent_appointments = Appointment.query.filter_by(priority='urgent', status='scheduled').count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'total_appointments': total_appointments,
                'scheduled_appointments': scheduled_appointments,
                'urgent_appointments': urgent_appointments
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'success': False,
        'error': 'Bad request'
    }), 400


# ============== INITIALIZE DATABASE ==============

def init_db():
    """Initialize database with sample data"""
    from models import Patient, Doctor, Appointment
    from datetime import datetime, timedelta
    
    with app.app_context():
        # Check if data already exists
        if Patient.query.first() is not None:
            print("Database already initialized with data.")
            return
        
        # Add sample doctors
        doctors = [
            Doctor(
                name='Dr. John Smith',
                specialization='Cardiology',
                contact='9876543210',
                email='john.smith@clinic.com',
                available_days='Monday, Tuesday, Wednesday, Thursday, Friday',
                start_time='09:00',
                end_time='17:00'
            ),
            Doctor(
                name='Dr. Sarah Johnson',
                specialization='Pediatrics',
                contact='9876543211',
                email='sarah.johnson@clinic.com',
                available_days='Monday, Wednesday, Friday',
                start_time='10:00',
                end_time='16:00'
            ),
            Doctor(
                name='Dr. Michael Brown',
                specialization='General Medicine',
                contact='9876543212',
                email='michael.brown@clinic.com',
                available_days='Monday, Tuesday, Wednesday, Thursday, Friday',
                start_time='08:00',
                end_time='18:00'
            ),
            Doctor(
                name='Dr. Emily Davis',
                specialization='Dermatology',
                contact='9876543213',
                email='emily.davis@clinic.com',
                available_days='Tuesday, Thursday, Saturday',
                start_time='11:00',
                end_time='19:00'
            ),
        ]
        
        for doctor in doctors:
            db.session.add(doctor)
        
        db.session.commit()
        
        # Add sample patients
        patients = [
            Patient(
                name='Alice Williams',
                age=32,
                contact='8765432101',
                email='alice.williams@email.com',
                address='123 Main St, City'
            ),
            Patient(
                name='Bob Miller',
                age=45,
                contact='8765432102',
                email='bob.miller@email.com',
                address='456 Oak Ave, City'
            ),
            Patient(
                name='Carol Anderson',
                age=28,
                contact='8765432103',
                email='carol.anderson@email.com',
                address='789 Pine Rd, City'
            ),
            Patient(
                name='David Lee',
                age=55,
                contact='8765432104',
                email='david.lee@email.com',
                address='321 Elm St, City'
            ),
            Patient(
                name='Eve Martinez',
                age=38,
                contact='8765432105',
                email='eve.martinez@email.com',
                address='654 Maple Dr, City'
            ),
        ]
        
        for patient in patients:
            db.session.add(patient)
        
        db.session.commit()
        
        # Add sample appointments
        today = datetime.now().date()
        appointments = [
            Appointment(
                patient_id=1,
                doctor_id=1,
                appointment_date=today + timedelta(days=2),
                appointment_time='10:00',
                priority='normal',
                reason='Regular checkup',
                status='scheduled'
            ),
            Appointment(
                patient_id=2,
                doctor_id=3,
                appointment_date=today + timedelta(days=1),
                appointment_time='14:00',
                priority='urgent',
                reason='High fever',
                status='scheduled'
            ),
            Appointment(
                patient_id=3,
                doctor_id=2,
                appointment_date=today + timedelta(days=3),
                appointment_time='11:00',
                priority='normal',
                reason='Child vaccination',
                status='scheduled'
            ),
            Appointment(
                patient_id=4,
                doctor_id=1,
                appointment_date=today + timedelta(days=5),
                appointment_time='15:00',
                priority='normal',
                reason='Heart checkup',
                status='scheduled'
            ),
            Appointment(
                patient_id=5,
                doctor_id=4,
                appointment_date=today + timedelta(days=4),
                appointment_time='16:00',
                priority='normal',
                reason='Skin consultation',
                status='scheduled'
            ),
        ]
        
        for appointment in appointments:
            db.session.add(appointment)
        
        db.session.commit()
        
        print("Database initialized with sample data!")
        print(f"  - {len(doctors)} doctors added")
        print(f"  - {len(patients)} patients added")
        print(f"  - {len(appointments)} appointments added")


# ============== RUN APPLICATION ==============

if __name__ == '__main__':
    # Initialize database with sample data on first run
    init_db()
    
    # Run the Flask app
    print("=" * 60)
    print("Smart Clinic Management System")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='localhost', port=5000)
