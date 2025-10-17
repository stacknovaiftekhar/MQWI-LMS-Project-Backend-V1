# 📘 Markazul Quran Wassunnah Institute (MQWI) - LMS Backend

**Learning Management System (LMS) Backend** built for **Markazul Quran Wassunnah Institute** using **Python**, **Django**, and **Django REST Framework (DRF)**.
This backend powers the complete academic management system for the institute — enabling online courses, teacher-student management, enrollments, payments, invoices, and much more.

---

## 🚀 Features

- **User Management (Admin, Teachers, Students)**
  - Custom User Model with role-based access
  - JWT Authentication (Login, Registration, Token Refresh)

- **Course Management**
  - CRUD for Categories, Courses, Modules, and Lessons
  - Nested Serializers for hierarchical data
  - Lesson completion tracking

- **Enrollment System**
  - Course Enrollment with payment validation
  - Monthly subscription-based continuation
  - Linked payments and invoices

- **Payment & Invoice Management**
  - Registration and Monthly Payments via various gateways (Bkash, Nagad, Rocket, Islami)
  - Auto PDF invoice generation using **weasyprint**
  - Invoice email delivery system

- **Admin Dashboard API**
  - Centralized API endpoints for managing Teachers, Students, Categories, Courses, Enrollments, Payments, and Sadaqah

- **Support & Contact API**
  - Message system for users to contact institute administration
  - Support ticket tracking

---

## 🛠️ Technologies Used

### **Core Framework**
- Python 3.11
- Django 5.x
- Django REST Framework (DRF)

### **Authentication & Security**
- djangorestframework-simplejwt (JWT Authentication)
- django-cors-headers

### **Database**
- MySQL

### **PDF & Email**
- weasyprint (for PDF Invoice Generation)
- smtplib / EmailMessage (for sending emails)

### **Deployment & Server**
- Passenger + LiteSpeed (on cPanel)
- Static & Media configuration via `.htaccess`

---
