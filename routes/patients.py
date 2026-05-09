"""
Patient routes for CRUD operations
"""

from flask import request, jsonify
from . import patient_bp
from models import db, Patient


@patient_bp.route('/', methods=['GET'])
def get_all_patients():
    """Get all patients"""
    try:
        patients = Patient.query.all()
        return jsonify({
            'success': True,
            'data': [patient.to_dict() for patient in patients],
            'count': len(patients)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@patient_bp.route('/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
        
        return jsonify({
            'success': True,
            'data': patient.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@patient_bp.route('/', methods=['POST'])
def add_patient():
    """Add a new patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('age') or not data.get('contact'):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name, age, contact'
            }), 400
        
        # Check if patient with same contact already exists
        existing = Patient.query.filter_by(contact=data['contact']).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'Patient with this contact already exists'
            }), 400
        
        # Create new patient
        patient = Patient(
            name=data.get('name'),
            age=data.get('age'),
            contact=data.get('contact'),
            email=data.get('email', ''),
            address=data.get('address', '')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Patient added successfully',
            'data': patient.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@patient_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient information"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            patient.name = data['name']
        if 'age' in data:
            patient.age = data['age']
        if 'email' in data:
            patient.email = data['email']
        if 'address' in data:
            patient.address = data['address']
        # Note: contact cannot be changed as it's unique
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Patient updated successfully',
            'data': patient.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@patient_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient"""
    try:
        patient = Patient.query.get(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404
        
        db.session.delete(patient)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Patient deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@patient_bp.route('/search', methods=['GET'])
def search_patient():
    """Search patients by name or contact"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query required'
            }), 400
        
        # Search by name or contact
        patients = Patient.query.filter(
            (Patient.name.ilike(f'%{query}%')) |
            (Patient.contact.ilike(f'%{query}%'))
        ).all()
        
        return jsonify({
            'success': True,
            'data': [patient.to_dict() for patient in patients],
            'count': len(patients)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
