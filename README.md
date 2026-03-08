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

Python,
Django,
Django REST Framework,
PostgreSQL or SQLite (for development),
JWT Authentication (SimpleJWT),
SMTP Email integration(Gmail)
Swagger/ OpenAPI documentation

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
# How the System Works

Service providers are created through the admin panel.
Each provider has working hours.
A slot generation function creates time slots automatically for a number of days ahead.
Users can view available slots and book one through the API.
Once a slot is booked it becomes unavailable for others.
When a booking is created or cancelled, the system sends an email notification to the user.

# Installation

clone the repository
```
git clone https://github.com/Ysomnathsarkar544-ctrl/appointment-booking-system.git
cd appointment-booking-system
```
Create a virtual enviroment
```
python -m venv venv

```
Activate the enviroment
windows
```
venv\Scripts\activate

```
Install dependencies
```
pip install -r requirements.txt

```
Run migrations
```
python manage.py migrate

```
Create an admin user
```
python manage.py createsuperuser
```
Start the development server 
```
python manage.py runserver

```
# API Documentation
Swagger documentation is available at:
```
http://127.0.0.1:8000/swagger/

```
This interface allows you to explore and test all available endpoints.

# Example API Requests

#GET JWT Token
POST/api/token/
Request body
```
{
   "userame":"username",
    "password":"password"
}
```
#Book an Appointment
POST/api/bookings/book/
Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```
Body
```
{
  "slot_id":4
}
```
#Cancel Appointment
POST/api/bookings/cancel/
Body
```
{
 "appointment_id"10
}
```
#Admin Panel
The admin dashboard allows management of:
users,
Service Providers,
Time Slots,
Appointments

Admin URL
```
http://127.0.0.1:8000/admin/

```
# Future Improvements

Add Redis caching for slot availability
Background jobs for automatic slot generation using Celery
Rate limiting for booking endpoints
Better filtering for slot availability APIs

# Author

Somnath Sarkar

