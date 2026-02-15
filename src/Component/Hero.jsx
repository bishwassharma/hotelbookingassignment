import React, { useState, useEffect } from 'react';

const Hero = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1920&q=80',
      title: 'Welcome to Grand Hotel',
      subtitle: 'Experience Luxury Like Never Before'
    },
    {
      image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1920&q=80',
      title: 'Stunning Swimming Pool',
      subtitle: 'Relax in Our Crystal Clear Waters'
    },
    {
      image: 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=1920&q=80',
      title: 'Luxury Rooms',
      subtitle: 'Comfort and Elegance Combined'
    },
    {
      image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1920&q=80',
      title: 'Exquisite Dining',
      subtitle: 'Culinary Delights Await You'
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 2000);

    return () => clearInterval(interval);
  }, [slides.length]);

  const scrollToBooking = () => {
    const bookingSection = document.getElementById('booking');
    if (bookingSection) {
      bookingSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="home" className="hero">
      <div className="hero-slider">
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`hero-slide ${index === currentSlide ? 'active' : ''}`}
            style={{
              backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url('${slide.image}')`
            }}
          >
            <div className="hero-content">
              <h1>{slide.title}</h1>
              <p>{slide.subtitle}</p>
              <div className="hero-buttons">
                <button className="primary-btn" onClick={scrollToBooking}>
                  Book Your Stay
                </button>
                <button className="secondary-btn" onClick={() => document.getElementById('rooms')?.scrollIntoView({ behavior: 'smooth' })}>
                  Explore Rooms
                </button>
              </div>
            </div>
          </div>
        ))}
        <div className="hero-dots">
          {slides.map((_, index) => (
            <span
              key={index}
              className={`dot ${index === currentSlide ? 'active' : ''}`}
              onClick={() => setCurrentSlide(index)}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Hero;
