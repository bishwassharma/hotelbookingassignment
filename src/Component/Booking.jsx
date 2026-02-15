import React, { useState } from 'react';

const Booking = () => {
  const [bookingData, setBookingData] = useState({
    checkIn: '',
    checkOut: '',
    guests: '2',
    roomType: 'deluxe'
  });

  const handleChange = (e) => {
    setBookingData({
      ...bookingData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Booking Request Submitted!\n\nCheck-in: ${bookingData.checkIn}\nCheck-out: ${bookingData.checkOut}\nGuests: ${bookingData.guests}\nRoom Type: ${bookingData.roomType}\n\nOur team will contact you shortly to confirm your reservation.`);
  };

  return (
    <section id="booking" className="booking">
      <div className="container">
        <h2 className="section-title">Book Your Stay</h2>
        <p className="section-subtitle">Reserve your perfect room today</p>
        <form className="booking-form" onSubmit={handleSubmit}>
          <div className="booking-row">
            <div className="booking-field">
              <label htmlFor="checkIn">Check-in Date</label>
              <input
                type="date"
                id="checkIn"
                name="checkIn"
                value={bookingData.checkIn}
                onChange={handleChange}
                required
              />
            </div>
            <div className="booking-field">
              <label htmlFor="checkOut">Check-out Date</label>
              <input
                type="date"
                id="checkOut"
                name="checkOut"
                value={bookingData.checkOut}
                onChange={handleChange}
                required
              />
            </div>
            <div className="booking-field">
              <label htmlFor="guests">Number of Guests</label>
              <select
                id="guests"
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
            <div className="booking-field">
              <label htmlFor="roomType">Room Type</label>
              <select
                id="roomType"
                name="roomType"
                value={bookingData.roomType}
                onChange={handleChange}
              >
                <option value="deluxe">Deluxe Room - $199/night</option>
                <option value="executive">Executive Suite - $349/night</option>
                <option value="presidential">Presidential Suite - $799/night</option>
              </select>
            </div>
          </div>
          <button type="submit" className="booking-btn">Check Availability & Book</button>
        </form>
      </div>
    </section>
  );
};

export default Booking;
