import React from 'react';
import { Navigate } from 'react-router-dom';
import { useCurrentAuthenticatedUser } from '../hooks/auth/useGetcurrentUser';

const PrivateRoutes = ({ children, allowedRoles }) => {
  const { data: user, isLoading, error } = useCurrentAuthenticatedUser();
  const isAuthenticated = !!user;
  const userRole = user?.role; // Assuming user object has a 'role' field

  if (isLoading) {
    return <div>Loading...</div>; // Show loading state while fetching user data
  }

  if (error || !isAuthenticated) {
    return <Navigate to="/sign-in" replace />; // Redirect to sign-in if unauthenticated
  }

  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <Navigate to="/" replace />; // Redirect to homepage if role is not allowed
  }

  return children;
};

export default PrivateRoutes