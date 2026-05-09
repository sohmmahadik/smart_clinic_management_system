"""
Utility functions for appointment scheduling and logic
"""

from datetime import datetime, timedelta
from .models import Appointment, Doctor
from . import db


def check_doctor_availability(doctor_id, appointment_date, appointment_time):
    """
    Check if doctor is available at the given date and time.
    
    Args:
        doctor_id: ID of the doctor
        appointment_date: Date of appointment (YYYY-MM-DD format or date object)
        appointment_time: Time of appointment (HH:MM format)
    
    Returns:
        tuple: (is_available: bool, message: str)
    """
    
    # Convert string date to date object if needed
    if isinstance(appointment_date, str):
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    # Get doctor
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return False, "Doctor not found"
    
    # Check if date is in the past
    if appointment_date < datetime.now().date():
        return False, "Cannot book appointment for a past date"
    
    # Check available days
    available_days = [day.strip() for day in doctor.available_days.split(',')]
    day_name = appointment_date.strftime('%A')
    if day_name not in available_days:
        return False, f"Doctor is not available on {day_name}s"
    
    # Check if time is within doctor's working hours
    try:
        app_time = datetime.strptime(appointment_time, '%H:%M').time()
        start_time = datetime.strptime(doctor.start_time, '%H:%M').time()
        end_time = datetime.strptime(doctor.end_time, '%H:%M').time()
        
        if not (start_time <= app_time < end_time):
            return False, f"Time must be between {doctor.start_time} and {doctor.end_time}"
    except ValueError:
        return False, "Invalid time format. Use HH:MM"
    
    # Check for existing appointments (prevent double booking)
    existing = Appointment.query.filter_by(
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status='scheduled'
    ).first()
    
    if existing:
        return False, "This time slot is already booked"
    
    return True, "Doctor is available"


def suggest_next_available_slot(doctor_id, preferred_date=None):
    """
    Suggest the next available appointment slot for a doctor.
    
    Args:
        doctor_id: ID of the doctor
        preferred_date: Preferred date (YYYY-MM-DD format or date object), defaults to today
    
    Returns:
        dict: Contains available_date, available_time, or None if no slots found
    """
    
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return None
    
    # Set preferred date
    if preferred_date is None:
        current_date = datetime.now().date()
    else:
        if isinstance(preferred_date, str):
            current_date = datetime.strptime(preferred_date, '%Y-%m-%d').date()
        else:
            current_date = preferred_date
    
    # Ensure we start from today or later
    if current_date < datetime.now().date():
        current_date = datetime.now().date()
    
    available_days = [day.strip() for day in doctor.available_days.split(',')]
    
    # Search for available slots in the next 30 days
    for days_ahead in range(30):
        check_date = current_date + timedelta(days=days_ahead)
        day_name = check_date.strftime('%A')
        
        if day_name not in available_days:
            continue
        
        # Try hourly slots during working hours
        start_time = datetime.strptime(doctor.start_time, '%H:%M')
        end_time = datetime.strptime(doctor.end_time, '%H:%M')
        
        while start_time < end_time:
            time_str = start_time.strftime('%H:%M')
            
            # Check if slot is available
            existing = Appointment.query.filter_by(
                doctor_id=doctor_id,
                appointment_date=check_date,
                appointment_time=time_str,
                status='scheduled'
            ).first()
            
            if not existing:
                return {
                    'date': check_date.strftime('%Y-%m-%d'),
                    'time': time_str,
                    'day': day_name
                }
            
            start_time += timedelta(hours=1)
    
    return None


def get_urgent_appointments():
    """Get all urgent appointments scheduled for today/upcoming dates"""
    today = datetime.now().date()
    urgent = Appointment.query.filter_by(priority='urgent', status='scheduled').filter(
        Appointment.appointment_date >= today
    ).all()
    return urgent


def check_appointment_conflicts(patient_id, appointment_date, appointment_time):
    """
    Check if patient has multiple appointments on the same day.
    (Optional: prevent double booking for same patient)
    
    Args:
        patient_id: ID of the patient
        appointment_date: Date of appointment
        appointment_time: Time of appointment
    
    Returns:
        bool: True if conflict exists
    """
    existing = Appointment.query.filter_by(
        patient_id=patient_id,
        appointment_date=appointment_date,
        status='scheduled'
    ).first()
    
    return existing is not None
