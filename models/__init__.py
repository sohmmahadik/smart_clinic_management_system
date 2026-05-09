# Models package
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Import models to make them available
from .models import Patient, Doctor, Appointment

__all__ = ['db', 'Patient', 'Doctor', 'Appointment']
