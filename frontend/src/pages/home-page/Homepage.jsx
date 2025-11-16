import React from 'react';
import Hero from '../../components//home/Hero';
import Features from '../../components//home/Features';


const Homepage = () => {

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <Hero />
        <Features />
      </main>
    </div>
  );
}

export default Homepage