# EdTech Backend System
## Overview
The EdTech Backend System is a backend application designed to manage users, courses, and instructors for an educational technology platform. It provides functionalities for user registration, authentication, course creation, and enrollment management.

## Table of Contents
* Overview
* Features
* Architecture
* Installation
* Usage
* Modules
  1. User Management
  2. Course Management
  3. Instructor Management
  4. Lerner Management
* Database Schema
* Logging

## Features
* User registration and authentication
* Role-based access control (Lerner, Instructor, Admin)
* Course creation and management
* Enrollment management for Lerners
* Password management and updates
* Logging for debugging and monitoring

## Architecture
The application is built using Python and SQLAlchemy for ORM. It follows a modular structure with separate modules for user, course, instructor, and lerner management. The database used is SQLite.

![Architecture Diagram](./screen_shots/flow_chart.png)

Installation


1. Create a virtual environment:
   ```
   poetry shell
   ```

2. Install dependencies:
   ```
   poetry install
   ``` 

3. Set up the database: Ensure the database name is configured in settings.py and run the initial migration scripts if any.

## Usage
1. Run the application:

    ```
        python man.py
    ```    
2. Follow the on-screen instructions:
   * Register as a new Lerner or Instructor
   * Log in as an existing user
   * Manage courses and enrollments


## Modules
### User Management
*File*: entity.py , user.py
*Description*: Handles user information updates.
*Functions*:
update_userinfo(db: Session, user_id: int, obj_in: Dict[str, Any]) -> Optional[UserInfo]
### Course Management
*File*: entity.py , course.py
*Description*: Defines the CourseInfo model and manages course-related operations.
*Classes*: CourseInfo
### Enrollment Management
*File:* enrollment.py, entity.py ,
*Description:* Defines the EnrollmentInfo model and manages instructor-related operations.
*Classes:* EnrollmentInfo 

## Database Schema
*UserInfo:* Stores user details including type, name, email, and password.
*CourseInfo:* Stores course details including name and timestamps.
*InstructorInfo:* Stores instructor details including courses and timestamps.
## Logging
Logging is configured using Python's logging module. Logs are generated for database operations and errors to help with debugging and monitoring.

