import React from 'react';
import { Routes, Route } from 'react-router-dom';
import PrivateRoutes from './PrivateRoutes';
import Homepage from '../pages/home-page/Homepage';
import SignIn from '../pages/Auth/SignIn';
import SignUp from '../pages/Auth/SignUp';

const AppRoutes = () => {
    return (
        <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Homepage />} />

            {/* Auth Routes */}
            <Route path="/sign-in" element={<SignIn  />} />
            <Route path="/sign-up" element={<SignUp />} />
        </Routes>
    )
}

export default AppRoutes