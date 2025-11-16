import React from 'react'

const AccessDenied = ({ navigate }) => (
    <div className="text-center p-12 bg-danger/10 text-danger rounded-xl border border-danger/50">
        <X className="h-10 w-10 mx-auto mb-4" />
        <h2 className="text-2xl font-bold">Access Denied</h2>
        <p className="text-foreground/70 mt-2">You do not have permission to view this page. Please log in with the correct credentials.</p>
        <button onClick={() => navigate('signin')} className="mt-4 bg-danger text-danger-foreground font-semibold px-6 py-2 rounded-lg hover:bg-danger/90 transition-colors">Go to Sign In</button>
    </div>
);

export default AccessDenied