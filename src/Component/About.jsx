import React from 'react';

const About = () => {
  return (
    <section id="about" className="about">
      <div className="container">
        <h2 className="section-title">About Us</h2>
        <div className="about-content">
          <div className="about-text">
            <p>
              Welcome to Grand Hotel, where luxury meets comfort. Established in 1995, 
              we have been providing exceptional hospitality to our guests for over two 
              decades. Our commitment to excellence and attention to detail has made us 
              a preferred choice for travelers seeking an unforgettable experience.
            </p>
            <p>
              Nestled in the heart of the city, our hotel offers a perfect blend of 
              modern amenities and classic elegance. Whether you're here for business 
              or leisure, our dedicated team is committed to making your stay memorable.
            </p>
            <div className="about-features">
              <div className="feature">
                <span className="feature-icon">★</span>
                <span>24/7 Concierge Service</span>
              </div>
              <div className="feature">
                <span className="feature-icon">★</span>
                <span>Premium Room Service</span>
              </div>
              <div className="feature">
                <span className="feature-icon">★</span>
                <span>World-Class Spa</span>
              </div>
              <div className="feature">
                <span className="feature-icon">★</span>
                <span>Award-Winning Dining</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
