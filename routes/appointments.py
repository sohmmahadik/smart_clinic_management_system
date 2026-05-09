"""
Appointment routes for CRUD operations and scheduling
"""

from flask import request, jsonify
from . import appointment_bp
from models import db, Appointment, Patient, Doctor
from models.utils import (
    check_doctor_availability,
    suggest_next_available_slot,
    get_urgent_appointments
)


@appointment_bp.route('/', methods=['GET'])
def get_all_appointments():
    """Get all appointments"""
    try:
        appointments = Appointment.query.all()
        return jsonify({
            'success': True,
            'data': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get a specific appointment by ID"""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
        
        return jsonify({
            'success': True,
            'data': appointment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/', methods=['POST'])
def book_appointment():
    """Book a new appointment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['patient_id', 'doctor_id', 'appointment_date', 'appointment_time']
        if not all(data.get(field) for field in required):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required)}'
            }), 400
        
        # Validate patient and doctor exist
        patient = Patient.query.get(data['patient_id'])
        doctor = Doctor.query.get(data['doctor_id'])
        
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        # Check doctor availability
        is_available, message = check_doctor_availability(
            data['doctor_id'],
            data['appointment_date'],
            data['appointment_time']
        )
        
        if not is_available:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Create appointment
        appointment = Appointment(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            priority=data.get('priority', 'normal').lower(),
            reason=data.get('reason', ''),
            notes=data.get('notes', '')
        )
        
        # Validate priority
        if appointment.priority not in ['urgent', 'normal']:
            appointment.priority = 'normal'
        
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Appointment booked successfully',
            'data': appointment.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update appointment information"""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'priority' in data:
            if data['priority'].lower() in ['urgent', 'normal']:
                appointment.priority = data['priority'].lower()
        
        if 'status' in data:
            if data['status'].lower() in ['scheduled', 'completed', 'cancelled']:
                appointment.status = data['status'].lower()
        
        if 'reason' in data:
            appointment.reason = data['reason']
        
        if 'notes' in data:
            appointment.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Appointment updated successfully',
            'data': appointment.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    """Cancel/delete an appointment"""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
        
        db.session.delete(appointment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Appointment cancelled successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_patient_appointments(patient_id):
    """Get all appointments for a specific patient"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
        
        appointments = Appointment.query.filter_by(patient_id=patient_id).all()
        
        return jsonify({
            'success': True,
            'data': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/doctor/<int:doctor_id>', methods=['GET'])
def get_doctor_appointments(doctor_id):
    """Get all appointments for a specific doctor"""
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
        
        return jsonify({
            'success': True,
            'data': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/suggest-slot/<int:doctor_id>', methods=['GET'])
def suggest_appointment_slot(doctor_id):
    """Suggest next available appointment slot for a doctor"""
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        preferred_date = request.args.get('date')
        slot = suggest_next_available_slot(doctor_id, preferred_date)
        
        if slot:
            return jsonify({
                'success': True,
                'data': slot
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No available slots found in the next 30 days'
            }), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@appointment_bp.route('/urgent-appointments', methods=['GET'])
def get_urgent_appts():
    """Get all urgent appointments"""
    try:
        appointments = get_urgent_appointments()
        
        return jsonify({
            'success': True,
            'data': [apt.to_dict() for apt in appointments],
            'count': len(appointments)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
