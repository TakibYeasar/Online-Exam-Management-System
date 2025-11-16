import React from 'react'

const NotFound = ({ navigate }) => {
  return (
      <div className="text-center p-12 bg-warning/10 text-warning-foreground rounded-xl border border-warning/50">
          <h2 className="text-2xl font-bold">404 - Page Not Found</h2>
          <p className="text-foreground/70 mt-2">The requested page does not exist.</p>
          <button onClick={() => navigate('home')} className="mt-4 bg-primary text-primary-foreground font-semibold px-6 py-2 rounded-lg hover:bg-primary/90 transition-colors">Go Home</button>
      </div>
  )
}

export default NotFound