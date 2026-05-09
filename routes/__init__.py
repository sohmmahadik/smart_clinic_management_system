# Routes package
from flask import Blueprint

# Create blueprints for different routes
patient_bp = Blueprint('patients', __name__, url_prefix='/api/patients')
doctor_bp = Blueprint('doctors', __name__, url_prefix='/api/doctors')
appointment_bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

# Import routes
from .patients import *
from .doctors import *
from .appointments import *

__all__ = ['patient_bp', 'doctor_bp', 'appointment_bp']
