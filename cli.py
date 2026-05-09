"""
Smart Clinic Management System - CLI Version (Alternative Interface)
Use this for command-line interaction without the web browser
"""

import os
import sys
from datetime import datetime, timedelta
from app import app, db, init_db
from models import Patient, Doctor, Appointment
from models.utils import (
    check_doctor_availability,
    suggest_next_available_slot,
    get_urgent_appointments
)

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display header
def show_header():
    clear_screen()
    print("=" * 70)
    print("🏥  SMART CLINIC MANAGEMENT SYSTEM - CLI VERSION")
    print("=" * 70)
    print()

# Display menu
def show_main_menu():
    show_header()
    print("Main Menu:")
    print("=" * 70)
    print("1. Patient Management")
    print("2. Doctor Management")
    print("3. Appointment Management")
    print("4. View Dashboard")
    print("5. Exit")
    print("=" * 70)
    choice = input("Enter your choice (1-5): ").strip()
    return choice

# ==================== PATIENT MANAGEMENT ====================

def show_patient_menu():
    show_header()
    print("Patient Management:")
    print("=" * 70)
    print("1. Add Patient")
    print("2. View All Patients")
    print("3. Search Patient")
    print("4. Update Patient")
    print("5. Delete Patient")
    print("6. Back to Main Menu")
    print("=" * 70)
    choice = input("Enter your choice (1-6): ").strip()
    return choice

def add_patient_cli():
    show_header()
    print("Add New Patient:")
    print("=" * 70)
    
    with app.app_context():
        try:
            name = input("Patient Full Name: ").strip()
            age = int(input("Age: "))
            contact = input("Contact Number (10 digits): ").strip()
            email = input("Email (optional): ").strip() or None
            address = input("Address (optional): ").strip() or None
            
            # Check if patient already exists
            if Patient.query.filter_by(contact=contact).first():
                print("❌ Patient with this contact already exists!")
                return
            
            patient = Patient(
                name=name,
                age=age,
                contact=contact,
                email=email,
                address=address
            )
            
            db.session.add(patient)
            db.session.commit()
            print(f"\n✅ Patient added successfully! (ID: {patient.id})")
        
        except ValueError:
            print("❌ Invalid input. Please try again.")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_all_patients_cli():
    show_header()
    
    with app.app_context():
        patients = Patient.query.all()
        
        if not patients:
            print("No patients found.")
            input("Press Enter to continue...")
            return
        
        print("All Patients:")
        print("=" * 70)
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Contact':<12} {'Email':<20}")
        print("-" * 70)
        
        for patient in patients:
            print(f"{patient.id:<5} {patient.name:<20} {patient.age:<5} {patient.contact:<12} {patient.email or '-':<20}")
        
        print("-" * 70)
        print(f"Total: {len(patients)} patient(s)")
    
    input("\nPress Enter to continue...")

def search_patient_cli():
    show_header()
    print("Search Patient:")
    print("=" * 70)
    
    query = input("Enter name or contact to search: ").strip()
    
    with app.app_context():
        patients = Patient.query.filter(
            (Patient.name.ilike(f'%{query}%')) |
            (Patient.contact.ilike(f'%{query}%'))
        ).all()
        
        if not patients:
            print("No patients found.")
        else:
            print(f"\nFound {len(patients)} patient(s):")
            print("=" * 70)
            print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Contact':<12}")
            print("-" * 70)
            
            for patient in patients:
                print(f"{patient.id:<5} {patient.name:<20} {patient.age:<5} {patient.contact:<12}")
    
    input("\nPress Enter to continue...")

def update_patient_cli():
    show_header()
    print("Update Patient:")
    print("=" * 70)
    
    with app.app_context():
        patient_id = int(input("Enter Patient ID: "))
        patient = Patient.query.get(patient_id)
        
        if not patient:
            print("❌ Patient not found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nCurrent Details:")
        print(f"Name: {patient.name}")
        print(f"Age: {patient.age}")
        print(f"Email: {patient.email or '-'}")
        print(f"Address: {patient.address or '-'}")
        print("=" * 70)
        
        name = input(f"New Name ({patient.name}): ").strip() or patient.name
        age = input(f"New Age ({patient.age}): ").strip()
        age = int(age) if age else patient.age
        email = input(f"New Email ({patient.email or '-'}): ").strip() or patient.email
        address = input(f"New Address ({patient.address or '-'}): ").strip() or patient.address
        
        patient.name = name
        patient.age = age
        patient.email = email
        patient.address = address
        
        db.session.commit()
        print("\n✅ Patient updated successfully!")
    
    input("\nPress Enter to continue...")

def delete_patient_cli():
    show_header()
    print("Delete Patient:")
    print("=" * 70)
    
    with app.app_context():
        patient_id = int(input("Enter Patient ID: "))
        patient = Patient.query.get(patient_id)
        
        if not patient:
            print("❌ Patient not found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nPatient: {patient.name}")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            db.session.delete(patient)
            db.session.commit()
            print("✅ Patient deleted successfully!")
        else:
            print("❌ Deletion cancelled.")
    
    input("\nPress Enter to continue...")

def manage_patients():
    while True:
        choice = show_patient_menu()
        
        if choice == '1':
            add_patient_cli()
        elif choice == '2':
            view_all_patients_cli()
        elif choice == '3':
            search_patient_cli()
        elif choice == '4':
            update_patient_cli()
        elif choice == '5':
            delete_patient_cli()
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice!")
            input("Press Enter to continue...")

# ==================== DOCTOR MANAGEMENT ====================

def show_doctor_menu():
    show_header()
    print("Doctor Management:")
    print("=" * 70)
    print("1. Add Doctor")
    print("2. View All Doctors")
    print("3. Search Doctor")
    print("4. Update Doctor")
    print("5. Delete Doctor")
    print("6. Back to Main Menu")
    print("=" * 70)
    choice = input("Enter your choice (1-6): ").strip()
    return choice

def add_doctor_cli():
    show_header()
    print("Add New Doctor:")
    print("=" * 70)
    
    with app.app_context():
        try:
            name = input("Doctor Full Name: ").strip()
            specialization = input("Specialization (e.g., Cardiology): ").strip()
            contact = input("Contact Number: ").strip()
            email = input("Email (optional): ").strip() or None
            available_days = input("Available Days (comma-separated, default: M-F): ").strip()
            if not available_days:
                available_days = "Monday, Tuesday, Wednesday, Thursday, Friday"
            start_time = input("Start Time (HH:MM, default: 09:00): ").strip() or "09:00"
            end_time = input("End Time (HH:MM, default: 17:00): ").strip() or "17:00"
            
            # Check if doctor already exists
            if Doctor.query.filter_by(contact=contact).first():
                print("❌ Doctor with this contact already exists!")
                return
            
            doctor = Doctor(
                name=name,
                specialization=specialization,
                contact=contact,
                email=email,
                available_days=available_days,
                start_time=start_time,
                end_time=end_time
            )
            
            db.session.add(doctor)
            db.session.commit()
            print(f"\n✅ Doctor added successfully! (ID: {doctor.id})")
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_all_doctors_cli():
    show_header()
    
    with app.app_context():
        doctors = Doctor.query.all()
        
        if not doctors:
            print("No doctors found.")
            input("Press Enter to continue...")
            return
        
        print("All Doctors:")
        print("=" * 70)
        print(f"{'ID':<3} {'Name':<20} {'Specialization':<18} {'Hours':<15}")
        print("-" * 70)
        
        for doctor in doctors:
            hours = f"{doctor.start_time}-{doctor.end_time}"
            print(f"{doctor.id:<3} {doctor.name:<20} {doctor.specialization:<18} {hours:<15}")
        
        print("-" * 70)
        print(f"Total: {len(doctors)} doctor(s)")
    
    input("\nPress Enter to continue...")

def search_doctor_cli():
    show_header()
    print("Search Doctor:")
    print("=" * 70)
    
    query = input("Enter name or specialization to search: ").strip()
    
    with app.app_context():
        doctors = Doctor.query.filter(
            (Doctor.name.ilike(f'%{query}%')) |
            (Doctor.specialization.ilike(f'%{query}%'))
        ).all()
        
        if not doctors:
            print("No doctors found.")
        else:
            print(f"\nFound {len(doctors)} doctor(s):")
            print("=" * 70)
            print(f"{'ID':<3} {'Name':<20} {'Specialization':<18}")
            print("-" * 70)
            
            for doctor in doctors:
                print(f"{doctor.id:<3} {doctor.name:<20} {doctor.specialization:<18}")
    
    input("\nPress Enter to continue...")

def update_doctor_cli():
    show_header()
    print("Update Doctor:")
    print("=" * 70)
    
    with app.app_context():
        doctor_id = int(input("Enter Doctor ID: "))
        doctor = Doctor.query.get(doctor_id)
        
        if not doctor:
            print("❌ Doctor not found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nCurrent Details:")
        print(f"Name: {doctor.name}")
        print(f"Specialization: {doctor.specialization}")
        print(f"Available Days: {doctor.available_days}")
        print(f"Hours: {doctor.start_time} - {doctor.end_time}")
        print("=" * 70)
        
        name = input(f"New Name ({doctor.name}): ").strip() or doctor.name
        specialization = input(f"New Specialization ({doctor.specialization}): ").strip() or doctor.specialization
        available_days = input(f"New Available Days ({doctor.available_days}): ").strip() or doctor.available_days
        start_time = input(f"New Start Time ({doctor.start_time}): ").strip() or doctor.start_time
        end_time = input(f"New End Time ({doctor.end_time}): ").strip() or doctor.end_time
        
        doctor.name = name
        doctor.specialization = specialization
        doctor.available_days = available_days
        doctor.start_time = start_time
        doctor.end_time = end_time
        
        db.session.commit()
        print("\n✅ Doctor updated successfully!")
    
    input("\nPress Enter to continue...")

def delete_doctor_cli():
    show_header()
    print("Delete Doctor:")
    print("=" * 70)
    
    with app.app_context():
        doctor_id = int(input("Enter Doctor ID: "))
        doctor = Doctor.query.get(doctor_id)
        
        if not doctor:
            print("❌ Doctor not found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nDoctor: Dr. {doctor.name}")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            db.session.delete(doctor)
            db.session.commit()
            print("✅ Doctor deleted successfully!")
        else:
            print("❌ Deletion cancelled.")
    
    input("\nPress Enter to continue...")

def manage_doctors():
    while True:
        choice = show_doctor_menu()
        
        if choice == '1':
            add_doctor_cli()
        elif choice == '2':
            view_all_doctors_cli()
        elif choice == '3':
            search_doctor_cli()
        elif choice == '4':
            update_doctor_cli()
        elif choice == '5':
            delete_doctor_cli()
        elif choice == '6':
            return
        else:
            print("❌ Invalid choice!")
            input("Press Enter to continue...")

# ==================== APPOINTMENT MANAGEMENT ====================

def show_appointment_menu():
    show_header()
    print("Appointment Management:")
    print("=" * 70)
    print("1. Book Appointment")
    print("2. View All Appointments")
    print("3. View Patient Appointments")
    print("4. View Doctor Appointments")
    print("5. Suggest Next Slot")
    print("6. View Urgent Appointments")
    print("7. Cancel Appointment")
    print("8. Back to Main Menu")
    print("=" * 70)
    choice = input("Enter your choice (1-8): ").strip()
    return choice

def book_appointment_cli():
    show_header()
    print("Book New Appointment:")
    print("=" * 70)
    
    with app.app_context():
        try:
            # Get patient
            patient_id = int(input("Patient ID: "))
            patient = Patient.query.get(patient_id)
            if not patient:
                print("❌ Patient not found!")
                input("Press Enter to continue...")
                return
            
            # Get doctor
            doctor_id = int(input("Doctor ID: "))
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                print("❌ Doctor not found!")
                input("Press Enter to continue...")
                return
            
            # Get date and time
            date_str = input("Appointment Date (YYYY-MM-DD): ")
            time_str = input("Appointment Time (HH:MM): ")
            priority = input("Priority (urgent/normal): ").lower()
            if priority not in ['urgent', 'normal']:
                priority = 'normal'
            reason = input("Reason for visit: ")
            
            # Check availability
            is_available, message = check_doctor_availability(doctor_id, date_str, time_str)
            
            if not is_available:
                print(f"❌ {message}")
                input("Press Enter to continue...")
                return
            
            # Create appointment
            appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=date_str,
                appointment_time=time_str,
                priority=priority,
                reason=reason
            )
            
            db.session.add(appointment)
            db.session.commit()
            
            print(f"\n✅ Appointment booked successfully!")
            print(f"Patient: {patient.name}")
            print(f"Doctor: Dr. {doctor.name}")
            print(f"Date: {date_str}")
            print(f"Time: {time_str}")
            print(f"Priority: {priority}")
        
        except ValueError:
            print("❌ Invalid input!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_all_appointments_cli():
    show_header()
    
    with app.app_context():
        appointments = Appointment.query.all()
        
        if not appointments:
            print("No appointments found.")
            input("Press Enter to continue...")
            return
        
        print("All Appointments:")
        print("=" * 100)
        print(f"{'ID':<3} {'Patient':<20} {'Doctor':<20} {'Date':<12} {'Time':<6} {'Priority':<8}")
        print("-" * 100)
        
        for apt in appointments:
            print(f"{apt.id:<3} {apt.patient.name:<20} {apt.doctor.name:<20} {str(apt.appointment_date):<12} {apt.appointment_time:<6} {apt.priority:<8}")
        
        print("-" * 100)
        print(f"Total: {len(appointments)} appointment(s)")
    
    input("\nPress Enter to continue...")

def view_patient_appointments_cli():
    show_header()
    print("Patient Appointments:")
    print("=" * 70)
    
    with app.app_context():
        patient_id = int(input("Enter Patient ID: "))
        patient = Patient.query.get(patient_id)
        
        if not patient:
            print("❌ Patient not found!")
            input("Press Enter to continue...")
            return
        
        appointments = Appointment.query.filter_by(patient_id=patient_id).all()
        
        if not appointments:
            print(f"No appointments found for {patient.name}")
        else:
            print(f"\nAppointments for {patient.name}:")
            print("=" * 80)
            print(f"{'ID':<3} {'Doctor':<20} {'Date':<12} {'Time':<6} {'Priority':<8} {'Status':<10}")
            print("-" * 80)
            
            for apt in appointments:
                print(f"{apt.id:<3} {apt.doctor.name:<20} {str(apt.appointment_date):<12} {apt.appointment_time:<6} {apt.priority:<8} {apt.status:<10}")
    
    input("\nPress Enter to continue...")

def view_doctor_appointments_cli():
    show_header()
    print("Doctor Appointments:")
    print("=" * 70)
    
    with app.app_context():
        doctor_id = int(input("Enter Doctor ID: "))
        doctor = Doctor.query.get(doctor_id)
        
        if not doctor:
            print("❌ Doctor not found!")
            input("Press Enter to continue...")
            return
        
        appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
        
        if not appointments:
            print(f"No appointments found for Dr. {doctor.name}")
        else:
            print(f"\nAppointments for Dr. {doctor.name}:")
            print("=" * 80)
            print(f"{'ID':<3} {'Patient':<20} {'Date':<12} {'Time':<6} {'Priority':<8} {'Status':<10}")
            print("-" * 80)
            
            for apt in appointments:
                print(f"{apt.id:<3} {apt.patient.name:<20} {str(apt.appointment_date):<12} {apt.appointment_time:<6} {apt.priority:<8} {apt.status:<10}")
    
    input("\nPress Enter to continue...")

def suggest_slot_cli():
    show_header()
    print("Suggest Next Available Slot:")
    print("=" * 70)
    
    with app.app_context():
        doctor_id = int(input("Enter Doctor ID: "))
        doctor = Doctor.query.get(doctor_id)
        
        if not doctor:
            print("❌ Doctor not found!")
            input("Press Enter to continue...")
            return
        
        slot = suggest_next_available_slot(doctor_id)
        
        if slot:
            print(f"\n✅ Next available slot for Dr. {doctor.name}:")
            print(f"Date: {slot['date']}")
            print(f"Time: {slot['time']}")
            print(f"Day: {slot['day']}")
        else:
            print(f"❌ No available slots found in the next 30 days for Dr. {doctor.name}")
    
    input("\nPress Enter to continue...")

def view_urgent_appointments_cli():
    show_header()
    
    with app.app_context():
        appointments = get_urgent_appointments()
        
        if not appointments:
            print("No urgent appointments at this time.")
        else:
            print(f"Urgent Appointments ({len(appointments)} total):")
            print("=" * 100)
            print(f"{'ID':<3} {'Patient':<20} {'Doctor':<20} {'Date':<12} {'Time':<6}")
            print("-" * 100)
            
            for apt in appointments:
                print(f"{apt.id:<3} {apt.patient.name:<20} {apt.doctor.name:<20} {str(apt.appointment_date):<12} {apt.appointment_time:<6}")
    
    input("\nPress Enter to continue...")

def cancel_appointment_cli():
    show_header()
    print("Cancel Appointment:")
    print("=" * 70)
    
    with app.app_context():
        appointment_id = int(input("Enter Appointment ID: "))
        appointment = Appointment.query.get(appointment_id)
        
        if not appointment:
            print("❌ Appointment not found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nAppointment Details:")
        print(f"Patient: {appointment.patient.name}")
        print(f"Doctor: Dr. {appointment.doctor.name}")
        print(f"Date: {appointment.appointment_date}")
        print(f"Time: {appointment.appointment_time}")
        
        confirm = input("\nAre you sure you want to cancel? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            db.session.delete(appointment)
            db.session.commit()
            print("✅ Appointment cancelled successfully!")
        else:
            print("❌ Cancellation aborted.")
    
    input("\nPress Enter to continue...")

def manage_appointments():
    while True:
        choice = show_appointment_menu()
        
        if choice == '1':
            book_appointment_cli()
        elif choice == '2':
            view_all_appointments_cli()
        elif choice == '3':
            view_patient_appointments_cli()
        elif choice == '4':
            view_doctor_appointments_cli()
        elif choice == '5':
            suggest_slot_cli()
        elif choice == '6':
            view_urgent_appointments_cli()
        elif choice == '7':
            cancel_appointment_cli()
        elif choice == '8':
            return
        else:
            print("❌ Invalid choice!")
            input("Press Enter to continue...")

# ==================== DASHBOARD ====================

def show_dashboard():
    show_header()
    
    with app.app_context():
        total_patients = Patient.query.count()
        total_doctors = Doctor.query.count()
        total_appointments = Appointment.query.count()
        scheduled = Appointment.query.filter_by(status='scheduled').count()
        urgent = Appointment.query.filter_by(priority='urgent', status='scheduled').count()
        
        print("📊 CLINIC STATISTICS")
        print("=" * 70)
        print(f"Total Patients:              {total_patients}")
        print(f"Total Doctors:               {total_doctors}")
        print(f"Total Appointments:          {total_appointments}")
        print(f"Scheduled Appointments:      {scheduled}")
        print(f"Urgent Cases:                {urgent}")
        print("=" * 70)
    
    input("\nPress Enter to continue...")

# ==================== MAIN PROGRAM ====================

def main():
    with app.app_context():
        # Initialize database if needed
        init_db()
    
    while True:
        choice = show_main_menu()
        
        if choice == '1':
            manage_patients()
        elif choice == '2':
            manage_doctors()
        elif choice == '3':
            manage_appointments()
        elif choice == '4':
            show_dashboard()
        elif choice == '5':
            print("\n👋 Thank you for using Smart Clinic Management System!")
            print("Goodbye!\n")
            break
        else:
            print("❌ Invalid choice! Please try again.")
            input("Press Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your input and try again.")
