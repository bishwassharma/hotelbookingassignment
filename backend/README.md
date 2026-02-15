# Hotel Booking System - Flask Backend

Complete backend implementation for a Hotel Booking System with user authentication, hotel management, room booking, and more.

## Features

- **User Authentication**: Registration, Login, Logout with session management
- **Password Security**: Secure password hashing using Werkzeug
- **SQLAlchemy Models**: Users, Hotels, Rooms, Bookings
- **CRUD Operations**: Full create, read, update, delete for all entities
- **Booking Management**: Create, view, confirm, and cancel bookings
- **Admin Dashboard**: Basic admin functionality
- **RESTful API**: JSON endpoints for frontend integration
- **Sample Data**: Pre-populated hotels and rooms

## Requirements

- Python 3.8+
- SQLite (included with Python)

## Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Production Mode

```bash
gunicorn app:app
```

## Database

The database is automatically created and initialized with sample data when you first run the app. A SQLite database file `hotel_booking.db` will be created.

## Routes

### Authentication
- `GET /` - Home page
- `GET /register` - Registration page
- `POST /register` - Register new user
- `GET /login` - Login page
- `POST /login` - Login user
- `GET /logout` - Logout user

### Dashboard & Profile
- `GET /dashboard` - User dashboard (requires login)
- `GET /profile` - User profile (requires login)
- `POST /profile` - Update profile (requires login)

### Hotels
- `GET /hotels` - List all hotels
- `GET /hotel/<id>` - Hotel details

### Rooms
- `GET /rooms` - List all rooms
- `GET /room/<id>` - Room details

### Bookings
- `GET /book` - Create booking page (requires login)
- `POST /book` - Create booking (requires login)
- `GET /booking/<id>` - Booking details (requires login)
- `GET /booking/<id>/confirm` - Confirm booking (requires login)
- `GET /booking/<id>/cancel` - Cancel booking (requires login)
- `GET /booking/confirmation/<id>` - Booking confirmation (requires login)

### API Endpoints (JSON)
- `GET /api/hotels` - Get all hotels
- `GET /api/hotel/<id>` - Get hotel details
- `GET /api/bookings` - Get user bookings (requires login)
- `POST /api/check-availability` - Check room availability

### Admin
- `GET /admin` - Admin dashboard (requires admin)
- `GET /admin/hotel/create` - Create hotel (requires admin)
- `GET /admin/room/create` - Create room (requires admin)

## Project Structure

```
backend/
├── app.py           # Main Flask application with all routes
├── models.py        # SQLAlchemy database models
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## Environment Variables

You can set the following environment variables:

- `SECRET_KEY` - Flask secret key (for sessions)
- `DATABASE_URL` - Database connection string (default: sqlite:///hotel_booking.db)

Example:
```bash
export SECRET_KEY=your-secret-key
export DATABASE_URL=sqlite:///hotel_booking.db
python app.py
```

## Template Files

This backend uses Jinja2 templates. You'll need to create the following template files in a `templates/` folder:

- `templates/index.html` - Home page
- `templates/register.html` - Registration page
- `templates/login.html` - Login page
- `templates/dashboard.html` - User dashboard
- `templates/profile.html` - User profile
- `templates/hotels.html` - Hotel list
- `templates/hotel_details.html` - Hotel details
- `templates/rooms.html` - Room list
- `templates/room_details.html` - Room details
- `templates/booking_form.html` - Booking form
- `templates/booking_details.html` - Booking details
- `templates/booking_confirmation.html` - Booking confirmation
- `templates/error.html` - Error page
- `templates/admin/dashboard.html` - Admin dashboard
- `templates/admin/hotel_form.html` - Hotel creation form
- `templates/admin/room_form.html` - Room creation form

## Notes

- The application uses Flask-Session for session management
- Passwords are hashed using SHA-256 via Werkzeug's `generate_password_hash`
- The database auto-initializes with sample hotels and rooms on first run
- CORS is enabled for frontend integration
