import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Grand Hotel</h3>
            <p>Experience luxury and comfort at its finest. Your perfect stay awaits.</p>
            <div className="social-links">
              <a href="#" className="social-link">Facebook</a>
              <a href="#" className="social-link">Instagram</a>
              <a href="#" className="social-link">Twitter</a>
            </div>
          </div>
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#about">About Us</a></li>
              <li><a href="#rooms">Rooms & Suites</a></li>
              <li><a href="#amenities">Amenities</a></li>
              <li><a href="#dining">Dining</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Services</h4>
            <ul>
              <li><a href="#">Spa & Wellness</a></li>
              <li><a href="#">Business Center</a></li>
              <li><a href="#">Event Planning</a></li>
              <li><a href="#">Airport Transfer</a></li>
              <li><a href="#">Concierge</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Contact</h4>
            <p>123 Grand Hotel Street<br />City Center, State 12345</p>
            <p>Phone: +1 (555) 123-4567</p>
            <p>Email: info@grandhotel.com</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 Grand Hotel. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
