"""
SQLAlchemy Models for Hotel Booking System
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Hotel(db.Model):
    """Hotel model for storing hotel information"""
    __tablename__ = 'hotels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    star_rating = db.Column(db.Integer, default=3)
    image_url = db.Column(db.String(500))
    amenities = db.Column(db.Text)  # JSON string of amenities
    check_in_time = db.Column(db.String(10), default='14:00')
    check_out_time = db.Column(db.String(10), default='11:00')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    rooms = db.relationship('Room', backref='hotel', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='hotel', lazy=True)
    
    def __repr__(self):
        return f'<Hotel {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'star_rating': self.star_rating,
            'image_url': self.image_url,
            'amenities': self.amenities,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time
        }


class Room(db.Model):
    """Room model for storing room information within hotels"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # single, double, suite, etc.
    description = db.Column(db.Text)
    price_per_night = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, default=2)
    image_url = db.Column(db.String(500))
    amenities = db.Column(db.Text)  # JSON string of room amenities
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='room', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('hotel_id', 'room_number', name='unique_room_number'),
    )
    
    def __repr__(self):
        return f'<Room {self.room_number} - {self.room_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'hotel_id': self.hotel_id,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'capacity': self.capacity,
            'image_url': self.image_url,
            'amenities': self.amenities,
            'is_available': self.is_available
        }


class Booking(db.Model):
    """Booking model for storing reservation information"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    guest_name = db.Column(db.String(100))
    guest_email = db.Column(db.String(120))
    guest_phone = db.Column(db.String(20))
    number_of_guests = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'hotel_id': self.hotel_id,
            'room_id': self.room_id,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'guest_phone': self.guest_phone,
            'number_of_guests': self.number_of_guests,
            'total_price': self.total_price,
            'status': self.status,
            'special_requests': self.special_requests,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'hotel': self.hotel.to_dict() if self.hotel else None,
            'room': self.room.to_dict() if self.room else None
        }
