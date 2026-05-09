#!/bin/bash
# Smart Clinic Management System - macOS/Linux Runner
# This script helps you run the application easily

clear

while true; do
    echo "============================================================"
    echo "Smart Clinic Management System - Launcher"
    echo "============================================================"
    echo ""
    echo "Choose how to run the application:"
    echo ""
    echo "1. Web Interface (Recommended) - http://localhost:5000"
    echo "2. CLI Interface (Command Line) - Terminal-based"
    echo "3. Install/Update Dependencies"
    echo "4. Reset Database"
    echo "5. Exit"
    echo ""
    
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            clear
            echo "Starting web server..."
            echo "Open your browser: http://localhost:5000"
            echo "Press Ctrl+C to stop"
            echo ""
            python3 app.py
            ;;
        2)
            clear
            echo "Starting CLI..."
            echo ""
            python3 cli.py
            ;;
        3)
            clear
            echo "Installing dependencies..."
            pip install -r requirements.txt
            echo ""
            echo "Done! All dependencies installed."
            read -p "Press Enter to continue..."
            clear
            ;;
        4)
            clear
            echo "Resetting database..."
            if [ -f clinic.db ]; then
                rm clinic.db
                echo "Database deleted."
            fi
            echo "Database will be recreated on next run."
            read -p "Press Enter to continue..."
            clear
            ;;
        5)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            read -p "Press Enter to continue..."
            clear
            ;;
    esac
done
