"""
Flask Backend for Hotel Booking System
Complete application with authentication, CRUD operations, and booking management
"""
import os
from datetime import datetime, date, timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_session import Session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Hotel, Room, Booking

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///hotel_booking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

# Initialize extensions
db.init_app(app)
Session(app)
CORS(app)

# =============================================================================
# DECORATORS
# =============================================================================

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        # Add admin check here if needed
        return f(*args, **kwargs)
    return decorated_function


# =============================================================================
# ROUTES - AUTHENTICATION
# =============================================================================

@app.route('/')
def home():
    """Home page route"""
    # Get featured hotels (top 6)
    featured_hotels = Hotel.query.filter_by(is_active=True).limit(6).all()
    return render_template('index.html', hotels=featured_hotels)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        
        if not email or '@' not in email:
            errors.append('Please enter a valid email address.')
        
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Your account has been deactivated.', 'error')
                return render_template('login.html')
            
            # Set session
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to dashboard or previous page
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout route"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))


# =============================================================================
# ROUTES - DASHBOARD & PROFILE
# =============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route - shows bookings and profile"""
    user = User.query.get(session['user_id'])
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.created_at.desc()).all()
    
    # Calculate statistics
    total_bookings = len(bookings)
    confirmed_bookings = len([b for b in bookings if b.status == 'confirmed'])
    pending_bookings = len([b for b in bookings if b.status == 'pending'])
    
    return render_template('dashboard.html', 
                         user=user, 
                         bookings=bookings,
                         total_bookings=total_bookings,
                         confirmed_bookings=confirmed_bookings,
                         pending_bookings=pending_bookings)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management route"""
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Update user profile
        user.first_name = request.form.get('first_name', '').strip()
        user.last_name = request.form.get('last_name', '').strip()
        user.phone = request.form.get('phone', '').strip()
        
        # Update password if provided
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if new_password:
            if len(new_password) < 6:
                flash('Password must be at least 6 characters.', 'error')
                return render_template('profile.html', user=user)
            
            if new_password != confirm_password:
                flash('Passwords do not match.', 'error')
                return render_template('profile.html', user=user)
            
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)


# =============================================================================
# ROUTES - HOTELS
# =============================================================================

@app.route('/hotels')
def hotels():
    """List all hotels with optional filters"""
    # Get query parameters
    city = request.args.get('city', '')
    star_rating = request.args.get('star_rating', type=int)
    search = request.args.get('search', '')
    
    # Build query
    query = Hotel.query.filter_by(is_active=True)
    
    if city:
        query = query.filter(Hotel.city.ilike(f'%{city}%'))
    
    if star_rating:
        query = query.filter(Hotel.star_rating >= star_rating)
    
    if search:
        query = query.filter(Hotel.name.ilike(f'%{search}%'))
    
    hotels = query.all()
    
    # Get unique cities for filter
    cities = db.session.query(Hotel.city).filter_by(is_active=True).distinct().all()
    cities = [c[0] for c in cities if c[0]]
    
    return render_template('hotels.html', hotels=hotels, cities=cities)


@app.route('/hotel/<int:hotel_id>')
def hotel_details(hotel_id):
    """Hotel details page route"""
    hotel = Hotel.query.get_or_404(hotel_id)
    
    # Get available rooms
    rooms = Room.query.filter_by(hotel_id=hotel_id, is_available=True).all()
    
    # Get hotel reviews (if you have a review model)
    # reviews = Review.query.filter_by(hotel_id=hotel_id).all()
    
    return render_template('hotel_details.html', hotel=hotel, rooms=rooms)


# =============================================================================
# ROUTES - ROOMS
# =============================================================================

@app.route('/rooms')
def rooms():
    """List all available rooms"""
    # Get query parameters
    hotel_id = request.args.get('hotel_id', type=int)
    room_type = request.args.get('room_type')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    capacity = request.args.get('capacity', type=int)
    
    # Build query
    query = Room.query.filter_by(is_available=True)
    
    if hotel_id:
        query = query.filter_by(hotel_id=hotel_id)
    
    if room_type:
        query = query.filter_by(room_type=room_type)
    
    if min_price:
        query = query.filter(Room.price_per_night >= min_price)
    
    if max_price:
        query = query.filter(Room.price_per_night <= max_price)
    
    if capacity:
        query = query.filter(Room.capacity >= capacity)
    
    rooms = query.all()
    
    # Get room types for filter
    room_types = db.session.query(Room.room_type).distinct().all()
    room_types = [r[0] for r in room_types if r[0]]
    
    return render_template('rooms.html', rooms=rooms, room_types=room_types)


@app.route('/room/<int:room_id>')
def room_details(room_id):
    """Room details page route"""
    room = Room.query.get_or_404(room_id)
    hotel = Hotel.query.get(room.hotel_id)
    
    # Check availability for date range
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    
    is_available = True
    if check_in and check_out:
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            # Check for overlapping bookings
            existing_booking = Booking.query.filter(
                Booking.room_id == room_id,
                Booking.status.in_(['pending', 'confirmed']),
                Booking.check_in_date < check_out_date,
                Booking.check_out_date > check_in_date
            ).first()
            
            is_available = not existing_booking
        except ValueError:
            pass
    
    return render_template('room_details.html', room=room, hotel=hotel, is_available=is_available)


# =============================================================================
# ROUTES - BOOKINGS
# =============================================================================

@app.route('/book', methods=['GET', 'POST'])
@login_required
def create_booking():
    """Create a new booking"""
    if request.method == 'POST':
        room_id = request.form.get('room_id', type=int)
        check_in = request.form.get('check_in')
        check_out = request.form.get('check_out')
        guest_name = request.form.get('guest_name', '').strip()
        guest_email = request.form.get('guest_email', '').strip()
        guest_phone = request.form.get('guest_phone', '').strip()
        number_of_guests = request.form.get('number_of_guests', type=int, default=1)
        special_requests = request.form.get('special_requests', '').strip()
        
        # Validation
        errors = []
        
        if not room_id:
            errors.append('Please select a room.')
        
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
            
            if check_in_date < date.today():
                errors.append('Check-in date cannot be in the past.')
            
            if check_out_date <= check_in_date:
                errors.append('Check-out date must be after check-in date.')
        except (ValueError, TypeError):
            errors.append('Please provide valid dates.')
        
        if not guest_name:
            errors.append('Please provide guest name.')
        
        if not guest_email:
            errors.append('Please provide guest email.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('create_booking'))
        
        # Get room and calculate price
        room = Room.query.get(room_id)
        if not room:
            flash('Room not found.', 'error')
            return redirect(url_for('hotels'))
        
        nights = (check_out_date - check_in_date).days
        total_price = room.price_per_night * nights
        
        # Check availability
        existing_booking = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.status.in_(['pending', 'confirmed']),
            Booking.check_in_date < check_out_date,
            Booking.check_out_date > check_in_date
        ).first()
        
        if existing_booking:
            flash('Room is not available for the selected dates.', 'error')
            return redirect(url_for('room_details', room_id=room_id))
        
        # Create booking
        booking = Booking(
            user_id=session['user_id'],
            hotel_id=room.hotel_id,
            room_id=room_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone,
            number_of_guests=number_of_guests,
            total_price=total_price,
            special_requests=special_requests,
            status='pending'
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking created successfully!', 'success')
        return redirect(url_for('booking_confirmation', booking_id=booking.id))
    
    # GET request - show booking form
    room_id = request.args.get('room_id', type=int)
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    
    room = None
    hotel = None
    
    if room_id:
        room = Room.query.get(room_id)
        if room:
            hotel = Hotel.query.get(room.hotel_id)
    
    return render_template('booking_form.html', room=room, hotel=hotel, 
                         check_in=check_in, check_out=check_out)


@app.route('/booking/<int:booking_id>')
@login_required
def booking_details(booking_id):
    """View booking details"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify ownership
    if booking.user_id != session['user_id']:
        flash('You do not have permission to view this booking.', 'error')
        return redirect(url_for('dashboard'))
    
    hotel = Hotel.query.get(booking.hotel_id)
    room = Room.query.get(booking.room_id)
    
    return render_template('booking_details.html', booking=booking, hotel=hotel, room=room)


@app.route('/booking/<int:booking_id>/confirm')
@login_required
def confirm_booking(booking_id):
    """Confirm a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify ownership
    if booking.user_id != session['user_id']:
        flash('You do not have permission to modify this booking.', 'error')
        return redirect(url_for('dashboard'))
    
    if booking.status != 'pending':
        flash('Booking cannot be confirmed.', 'error')
        return redirect(url_for('booking_details', booking_id=booking_id))
    
    booking.status = 'confirmed'
    db.session.commit()
    
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('booking_details', booking_id=booking_id))


@app.route('/booking/<int:booking_id>/cancel')
@login_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify ownership
    if booking.user_id != session['user_id']:
        flash('You do not have permission to modify this booking.', 'error')
        return redirect(url_for('dashboard'))
    
    if booking.status not in ['pending', 'confirmed']:
        flash('Booking cannot be cancelled.', 'error')
        return redirect(url_for('booking_details', booking_id=booking_id))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking cancelled successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/booking/confirmation/<int:booking_id>')
@login_required
def booking_confirmation(booking_id):
    """Booking confirmation page"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify ownership
    if booking.user_id != session['user_id']:
        flash('You do not have permission to view this booking.', 'error')
        return redirect(url_for('dashboard'))
    
    hotel = Hotel.query.get(booking.hotel_id)
    room = Room.query.get(booking.room_id)
    
    return render_template('booking_confirmation.html', booking=booking, hotel=hotel, room=room)


# =============================================================================
# API ROUTES (JSON)
# =============================================================================

@app.route('/api/hotels')
def api_hotels():
    """API endpoint to get hotels as JSON"""
    hotels = Hotel.query.filter_by(is_active=True).all()
    return jsonify([hotel.to_dict() for hotel in hotels])


@app.route('/api/hotel/<int:hotel_id>')
def api_hotel(hotel_id):
    """API endpoint to get hotel details as JSON"""
    hotel = Hotel.query.get_or_404(hotel_id)
    rooms = Room.query.filter_by(hotel_id=hotel_id, is_available=True).all()
    
    return jsonify({
        'hotel': hotel.to_dict(),
        'rooms': [room.to_dict() for room in rooms]
    })


@app.route('/api/bookings')
@login_required
def api_bookings():
    """API endpoint to get user bookings as JSON"""
    bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.created_at.desc()).all()
    return jsonify([booking.to_dict() for booking in bookings])


@app.route('/api/check-availability', methods=['POST'])
def api_check_availability():
    """API endpoint to check room availability"""
    data = request.get_json()
    
    room_id = data.get('room_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        
        existing_booking = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.status.in_(['pending', 'confirmed']),
            Booking.check_in_date < check_out_date,
            Booking.check_out_date > check_in_date
        ).first()
        
        return jsonify({
            'available': not existing_booking,
            'message': 'Room is available' if not existing_booking else 'Room is not available'
        })
    except ValueError:
        return jsonify({'available': False, 'message': 'Invalid date format'}), 400


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('error.html', error_code=404, message='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('error.html', error_code=500, message='Internal server error'), 500


# =============================================================================
# ADMIN ROUTES (Basic implementation)
# =============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_hotels = Hotel.query.count()
    total_rooms = Room.query.count()
    total_bookings = Booking.query.count()
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_hotels=total_hotels,
                         total_rooms=total_rooms,
                         total_bookings=total_bookings,
                         recent_bookings=recent_bookings)


@app.route('/admin/hotel/create', methods=['GET', 'POST'])
@admin_required
def admin_create_hotel():
    """Admin route to create hotel"""
    if request.method == 'POST':
        hotel = Hotel(
            name=request.form.get('name'),
            description=request.form.get('description'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            country=request.form.get('country'),
            star_rating=request.form.get('star_rating', type=int, default=3),
            image_url=request.form.get('image_url'),
            amenities=request.form.get('amenities'),
            check_in_time=request.form.get('check_in_time', '14:00'),
            check_out_time=request.form.get('check_out_time', '11:00')
        )
        
        db.session.add(hotel)
        db.session.commit()
        
        flash('Hotel created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/hotel_form.html')


@app.route('/admin/room/create', methods=['GET', 'POST'])
@admin_required
def admin_create_room():
    """Admin route to create room"""
    hotels = Hotel.query.filter_by(is_active=True).all()
    
    if request.method == 'POST':
        room = Room(
            hotel_id=request.form.get('hotel_id', type=int),
            room_number=request.form.get('room_number'),
            room_type=request.form.get('room_type'),
            description=request.form.get('description'),
            price_per_night=request.form.get('price_per_night', type=float),
            capacity=request.form.get('capacity', type=int, default=2),
            image_url=request.form.get('image_url'),
            amenities=request.form.get('amenities')
        )
        
        db.session.add(room)
        db.session.commit()
        
        flash('Room created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/room_form.html', hotels=hotels)


# =============================================================================
# DATABASE SETUP
# =============================================================================

def init_db():
    """Initialize database with sample data"""
    db.create_all()
    
    # Check if data exists
    if Hotel.query.first():
        return
    
    # Create sample hotels
    hotels = [
        Hotel(
            name='Grand Plaza Hotel',
            description='A luxurious 5-star hotel in the heart of the city with stunning views and world-class amenities.',
            address='123 Main Street',
            city='New York',
            country='USA',
            star_rating=5,
            image_url='https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
            amenities='WiFi,Pool,Spa,Gym,Restaurant,Room Service,Parking',
            check_in_time='14:00',
            check_out_time='11:00'
        ),
        Hotel(
            name='Seaside Resort',
            description='Beautiful beachfront resort with private beach access and tropical gardens.',
            address='456 Ocean Drive',
            city='Miami',
            country='USA',
            star_rating=4,
            image_url='https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
            amenities='WiFi,Pool,Beach,Spa,Restaurant,Bar,Water Sports',
            check_in_time='15:00',
            check_out_time='11:00'
        ),
        Hotel(
            name='Mountain View Lodge',
            description='Cozy mountain retreat with breathtaking views and outdoor activities.',
            address='789 Mountain Road',
            city='Denver',
            country='USA',
            star_rating=4,
            image_url='https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800',
            amenities='WiFi,Fireplace,Hiking,Restaurant,Spa,Parking',
            check_in_time='16:00',
            check_out_time='10:00'
        ),
        Hotel(
            name='City Center Inn',
            description='Modern hotel in downtown area, perfect for business travelers.',
            address='321 Downtown Ave',
            city='Chicago',
            country='USA',
            star_rating=3,
            image_url='https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
            amenities='WiFi,Gym,Business Center,Restaurant,Parking',
            check_in_time='14:00',
            check_out_time='12:00'
        ),
        Hotel(
            name='Desert Oasis Hotel',
            description='Luxurious desert resort with pool and spa facilities.',
            address='555 Desert Way',
            city='Phoenix',
            country='USA',
            star_rating=4,
            image_url='https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
            amenities='WiFi,Pool,Spa,Golf,Restaurant,Bar',
            check_in_time='14:00',
            check_out_time='11:00'
        ),
        Hotel(
            name='Lakeside Hotel',
            description='Serene lakeside hotel with fishing and boating activities.',
            address='888 Lake Street',
            city='Seattle',
            country='USA',
            star_rating=3,
            image_url='https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
            amenities='WiFi,Boating,Fishing,Hiking,Restaurant',
            check_in_time='15:00',
            check_out_time='11:00'
        )
    ]
    
    for hotel in hotels:
        db.session.add(hotel)
    
    db.session.commit()
    
    # Create sample rooms for each hotel
    room_types = [
        ('Standard Room', 99, 2),
        ('Deluxe Room', 149, 2),
        ('Suite', 249, 4),
        ('Executive Suite', 399, 4),
        ('Presidential Suite', 599, 6)
    ]
    
    for hotel in Hotel.query.all():
        for room_type, price, capacity in room_types:
            room = Room(
                hotel_id=hotel.id,
                room_number=f'{hotel.id}{room_types.index((room_type, price, capacity)) + 1}01',
                room_type=room_type,
                description=f'Comfortable {room_type.lower()} with modern amenities.',
                price_per_night=price,
                capacity=capacity,
                image_url='https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800',
                amenities='WiFi,TV,Air Conditioning,Private Bathroom',
                is_available=True
            )
            db.session.add(room)
    
    db.session.commit()
    print("Database initialized with sample data!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
