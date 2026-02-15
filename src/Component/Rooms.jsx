import React from 'react';

const rooms = [
  {
    id: 1,
    name: 'Deluxe Room',
    description: 'Spacious room with city views, king-sized bed, and modern amenities',
    price: '$199/night',
    features: ['King Bed', 'City View', 'Free Wi-Fi', 'Mini Bar', 'Room Service'],
    image: 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=600&q=80'
  },
  {
    id: 2,
    name: 'Executive Suite',
    description: 'Luxurious suite with separate living area, perfect for business travelers',
    price: '$349/night',
    features: ['King Bed', 'Living Room', 'Executive Lounge Access', 'Work Desk', 'Jacuzzi'],
    image: 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600&q=80'
  },
  {
    id: 3,
    name: 'Presidential Suite',
    description: 'Ultimate luxury with panoramic views, private terrace, and premium services',
    price: '$799/night',
    features: ['Master Bedroom', 'Living Room', 'Private Terrace', 'Butler Service', 'Spa Access'],
    image: 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&q=80'
  }
];

const Rooms = () => {
  return (
    <section id="rooms" className="rooms">
      <div className="container">
        <h2 className="section-title">Rooms & Suites</h2>
        <p className="section-subtitle">Choose from our selection of beautifully appointed rooms</p>
        <div className="rooms-grid">
          {rooms.map(room => (
            <div key={room.id} className="room-card">
              <div className="room-image">
                <img src={room.image} alt={room.name} className="room-img" />
              </div>
              <div className="room-content">
                <h3>{room.name}</h3>
                <p>{room.description}</p>
                <ul className="room-features">
                  {room.features.map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
                <div className="room-footer">
                  <span className="room-price">{room.price}</span>
                  <button className="book-btn" onClick={() => document.getElementById('booking')?.scrollIntoView({ behavior: 'smooth' })}>
                    Book Now
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Rooms;
