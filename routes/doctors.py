"""
Doctor routes for CRUD operations
"""

from flask import request, jsonify
from . import doctor_bp
from models import db, Doctor


@doctor_bp.route('/', methods=['GET'])
def get_all_doctors():
    """Get all doctors"""
    try:
        doctors = Doctor.query.all()
        return jsonify({
            'success': True,
            'data': [doctor.to_dict() for doctor in doctors],
            'count': len(doctors)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@doctor_bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get a specific doctor by ID"""
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        return jsonify({
            'success': True,
            'data': doctor.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@doctor_bp.route('/', methods=['POST'])
def add_doctor():
    """Add a new doctor"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('specialization') or not data.get('contact'):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name, specialization, contact'
            }), 400
        
        # Check if doctor with same contact already exists
        existing = Doctor.query.filter_by(contact=data['contact']).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Doctor with this contact already exists'
            }), 400
        
        # Create new doctor
        doctor = Doctor(
            name=data.get('name'),
            specialization=data.get('specialization'),
            contact=data.get('contact'),
            email=data.get('email', ''),
            available_days=data.get('available_days', 'Monday, Tuesday, Wednesday, Thursday, Friday'),
            start_time=data.get('start_time', '09:00'),
            end_time=data.get('end_time', '17:00')
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Doctor added successfully',
            'data': doctor.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@doctor_bp.route('/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update doctor information"""
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            doctor.name = data['name']
        if 'specialization' in data:
            doctor.specialization = data['specialization']
        if 'email' in data:
            doctor.email = data['email']
        if 'available_days' in data:
            doctor.available_days = data['available_days']
        if 'start_time' in data:
            doctor.start_time = data['start_time']
        if 'end_time' in data:
            doctor.end_time = data['end_time']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Doctor updated successfully',
            'data': doctor.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@doctor_bp.route('/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Delete a doctor"""
    try:
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return jsonify({'success': False, 'error': 'Doctor not found'}), 404
        
        db.session.delete(doctor)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Doctor deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@doctor_bp.route('/by-specialization/<specialization>', methods=['GET'])
def get_doctors_by_specialization(specialization):
    """Get doctors by specialization"""
    try:
        doctors = Doctor.query.filter(
            Doctor.specialization.ilike(f'%{specialization}%')
        ).all()
        
        return jsonify({
            'success': True,
            'data': [doctor.to_dict() for doctor in doctors],
            'count': len(doctors)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
