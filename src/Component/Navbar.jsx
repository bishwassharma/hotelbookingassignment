import React, { useState, useRef, useEffect } from 'react';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showDatePopup, setShowDatePopup] = useState(false);
  const [bookingData, setBookingData] = useState({
    checkIn: '',
    checkOut: '',
    guests: '2'
  });
  const popupRef = useRef(null);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
    setIsMenuOpen(false);
    setShowDatePopup(false);
  };

  const handleBookNowClick = () => {
    setShowDatePopup(!showDatePopup);
    setIsMenuOpen(false);
  };

  const handleChange = (e) => {
    setBookingData({
      ...bookingData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (bookingData.checkIn && bookingData.checkOut) {
      alert(`Booking Request Submitted!\n\nCheck-in: ${bookingData.checkIn}\nCheck-out: ${bookingData.checkOut}\nGuests: ${bookingData.guests}\n\nOur team will contact you shortly to confirm your reservation.`);
      setShowDatePopup(false);
      setBookingData({ checkIn: '', checkOut: '', guests: '2' });
    }
  };

  // Close popup when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (popupRef.current && !popupRef.current.contains(event.target)) {
        setShowDatePopup(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <h1>Grand Hotel</h1>
        </div>
        
        <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
          <ul className="navbar-links">
            <li><button onClick={() => scrollToSection('home')}>Home</button></li>
            <li><button onClick={() => scrollToSection('about')}>About</button></li>
            <li><button onClick={() => scrollToSection('rooms')}>Rooms & Suites</button></li>
            <li><button onClick={() => scrollToSection('amenities')}>Amenities</button></li>
            <li><button onClick={() => scrollToSection('dining')}>Dining</button></li>
            <li><button onClick={() => scrollToSection('contact')}>Contact Us</button></li>
          </ul>
          <div className="book-now-container" ref={popupRef}>
            <button className="book-now-btn" onClick={handleBookNowClick}>
              Book Now
            </button>
            {showDatePopup && (
              <div className="date-popup">
                <form onSubmit={handleSubmit}>
                  <div className="popup-field">
                    <label htmlFor="popup-checkIn">Check-in</label>
                    <input
                      type="date"
                      id="popup-checkIn"
                      name="checkIn"
                      value={bookingData.checkIn}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="popup-field">
                    <label htmlFor="popup-checkOut">Check-out</label>
                    <input
                      type="date"
                      id="popup-checkOut"
                      name="checkOut"
                      value={bookingData.checkOut}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="popup-field">
                    <label htmlFor="popup-guests">Guests</label>
                    <select
                      id="popup-guests"
                      name="guests"
                      value={bookingData.guests}
                      onChange={handleChange}
                    >
                      <option value="1">1 Guest</option>
                      <option value="2">2 Guests</option>
                      <option value="3">3 Guests</option>
                      <option value="4">4 Guests</option>
                      <option value="5+">5+ Guests</option>
                    </select>
                  </div>
                  <button type="submit" className="popup-submit-btn">Check Availability</button>
                </form>
              </div>
            )}
          </div>
        </div>

        <button 
          className="navbar-toggle" 
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
