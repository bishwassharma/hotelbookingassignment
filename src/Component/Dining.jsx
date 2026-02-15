import React from 'react';

const diningOptions = [
  {
    name: 'The Grand Restaurant',
    type: 'Fine Dining',
    description: 'Award-winning fine dining restaurant offering international cuisine with a focus on local ingredients',
    hours: 'Breakfast: 6:30 AM - 10:30 AM | Dinner: 6:00 PM - 11:00 PM',
    cuisine: 'International',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80'
  },
  {
    name: 'Sky Lounge',
    type: 'Rooftop Bar',
    description: 'Stunning rooftop bar with panoramic city views, perfect for cocktails and light bites',
    hours: '4:00 PM - 1:00 AM',
    cuisine: 'Tapas & Cocktails',
    image: 'https://images.unsplash.com/photo-1470337458703-46ad1756a187?w=600&q=80'
  },
  {
    name: 'Café Delights',
    type: 'Casual Café',
    description: 'Cozy café serving fresh pastries, sandwiches, and premium coffee throughout the day',
    hours: '7:00 AM - 9:00 PM',
    cuisine: 'Bakery & Coffee',
    image: 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&q=80'
  },
  {
    name: 'Poolside Grill',
    type: 'Pool Bar & Grill',
    description: 'Relaxed poolside dining with grilled specialties and refreshing beverages',
    hours: '11:00 AM - 7:00 PM',
    cuisine: 'Grill & Bar',
    image: 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=600&q=80'
  }
];

const Dining = () => {
  return (
    <section id="dining" className="dining">
      <div className="container">
        <h2 className="section-title">Dining Experience</h2>
        <p className="section-subtitle">Culinary excellence awaits at our restaurants and bars</p>
        <div className="dining-grid">
          {diningOptions.map((venue, index) => (
            <div key={index} className="dining-card">
              <div className="dining-image">
                <img src={venue.image} alt={venue.name} />
              </div>
              <div className="dining-content">
                <h3>{venue.name}</h3>
                <span className="dining-type">{venue.cuisine}</span>
                <p>{venue.description}</p>
                <div className="dining-hours">
                  <strong>Hours:</strong> {venue.hours}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Dining;
