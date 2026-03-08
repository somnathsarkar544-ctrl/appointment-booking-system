# Appointment Booking System (Django REST API)

This project is a backend appointment booking system built with Django and Django REST Framework. It allows users to view available time slots, book appointments with different service providers, and receive email notifications for booking confirmations and cancellations.

The goal of this project was to design a simple but realistic scheduling system similar to platforms used by clinics, salons, or service-based businesses.

# Features

User authentication using JWT
Multiple service providers (for example Doctor and Salon)
Automatic generation of time slots
Booking appointments through REST APIs
Prevention of double booking for the same slot
Appointment cancellation
Email notifications for booking confirmation and cancellation
Admin panel for managing providers, slots, and appointments
Swagger API documentation

# Technology Stack

Python
Django
Django REST Framework
PostgreSQL or SQLite (for development)
JWT Authentication (SimpleJWT)

# Project Structure
```
appointment_system/
│
├── accounts/        User authentication and user APIs
├── bookings/        Appointment and time slot management
├── services/        Service providers and scheduling logic
├── core/            Project settings and configuration
├── templates/       Email templates
│
├── manage.py
└── requirements.txt
```
SMTP Email integration (Gmail)
Swagger / OpenAPI documentation
#
