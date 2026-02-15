import React from 'react';

const amenities = [
  {
    icon: '🏊',
    title: 'Swimming Pool',
    description: 'Infinity pool with stunning views',
    image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1920&q=80'
  },
  {
    icon: '💆',
    title: 'Spa & Wellness',
    description: 'Full-service spa with massages and treatments',
    image: 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600&q=80'
  },
  {
    icon: '🏋️',
    title: 'Fitness Center',
    description: 'State-of-the-art gym equipment',
    image: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80'
  },
  {
    icon: '🍽️',
    title: 'Restaurant',
    description: 'Fine dining with international cuisine',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80'
  },
  {
    icon: '🍸',
    title: 'Bar & Lounge',
    description: 'Craft cocktails and live music',
    image: 'https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=600&q=80'
  },
  {
    icon: '🚗',
    title: 'Valet Parking',
    description: 'Complimentary valet service',
    image: 'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?w=600&q=80'
  },
  {
    icon: '📋',
    title: 'Business Center',
    description: 'Meeting rooms and office services',
    image: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=80'
  },
  {
    icon: '🛎️',
    title: '24/7 Concierge',
    description: 'Round-the-clock assistance',
    image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80'
  }
];

const Amenities = () => {
  return (
    <section id="amenities" className="amenities">
      <div className="container">
        <h2 className="section-title">Our Amenities</h2>
        <p className="section-subtitle">Experience world-class amenities during your stay</p>
        <div className="amenities-grid">
          {amenities.map((amenity, index) => (
            <div key={index} className="amenity-card">
              <div className="amenity-image">
                <img src={amenity.image} alt={amenity.title} />
              </div>
              <span className="amenity-icon">{amenity.icon}</span>
              <h3>{amenity.title}</h3>
              <p>{amenity.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Amenities;
