import React from 'react';
import { Routes, Route } from 'react-router-dom';
import PrivateRoutes from './PrivateRoutes';
import Homepage from '../pages/home-page/Homepage';
import AdminDashboard from '../pages/dashboard/admin/AdminDashboard';
import StudentDashboard from '../pages/dashboard/student/StudentDashboard';
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

            {/* Role-Based Protected Routes */}
            <Route
                path="/admin-dashboard"
                element={
                    <PrivateRoutes allowedRoles={['admin']}>
                        <AdminDashboard />
                    </PrivateRoutes>
                }
            />
            <Route
                path="/student-dashboard"
                element={
                    <PrivateRoutes allowedRoles={['student']}>
                        <StudentDashboard />
                    </PrivateRoutes>
                }
            />
        </Routes>
    )
}

export default AppRoutes