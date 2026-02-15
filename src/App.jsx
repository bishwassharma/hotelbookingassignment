import React from 'react';
import Navbar from './Component/Navbar';
import Hero from './Component/Hero';
import About from './Component/About';
import Rooms from './Component/Rooms';
import Amenities from './Component/Amenities';
import Dining from './Component/Dining';
import Contact from './Component/Contact';
import Booking from './Component/Booking';
import Footer from './Component/Footer';

function App() {
  return (
    <div className="app">
      <Navbar />
      <Hero />
      <About />
      <Rooms />
      <Amenities />
      <Dining />
      <Booking />
      <Contact />
      <Footer />
    </div>
  );
}

export default App;
