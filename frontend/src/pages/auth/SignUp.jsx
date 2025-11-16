import React, { useState } from 'react';
import { Mail, Lock, User, Globe } from 'lucide-react';
import AuthInput from '../../components/common/AuthInput';

const SignUp = ({ onSwitchToSignIn = () => console.log('Switch to Sign In triggered.') }) => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            return;
        }
        console.log('Sign Up Data:', formData);
    };

    const title = 'Create an Account';
    const description = 'Register below to start setting up or taking exams.';

    return (
        <div className="flex items-center justify-center min-h-screen bg-background p-4 sm:p-6">
            <div className="w-full max-w-lg p-6 sm:p-8 bg-card rounded-2xl shadow-2xl border border-border">

                {/* Logo and Header */}
                <div className="flex flex-col items-center space-y-2 mb-8">
                    <Globe className="h-10 w-10 text-primary" />
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">{title}</h1>
                    <p className="text-sm text-foreground/70 text-center">{description}</p>
                </div>

                <form onSubmit={handleSubmit} className="w-full max-w-md space-y-6 mx-auto">
                    <AuthInput
                        id="name"
                        label="Full Name"
                        type="text"
                        icon={User}
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="John Doe"
                    />
                    <AuthInput
                        id="email"
                        label="Email Address"
                        type="email"
                        icon={Mail}
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="you@example.com"
                    />
                    <AuthInput
                        id="password"
                        label="Password"
                        type="password"
                        icon={Lock}
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Set a secure password"
                    />
                    <AuthInput
                        id="confirmPassword"
                        label="Confirm Password"
                        type="password"
                        icon={Lock}
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        placeholder="Repeat your password"
                    />

                    <div className="flex items-start">
                        <input
                            id="terms"
                            name="terms"
                            type="checkbox"
                            required
                            className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary mt-1"
                        />
                        <label htmlFor="terms" className="ml-2 block text-sm text-foreground/80">
                            I agree to the <a href="#" className="font-medium text-primary hover:text-primary/80">Terms of Service</a> and <a href="#" className="font-medium text-primary hover:text-primary/80">Privacy Policy</a>.
                        </label>
                    </div>

                    <button
                        type="submit"
                        className="w-full justify-center rounded-md bg-success py-2 px-4 text-sm font-semibold text-success-foreground shadow-md hover:bg-success/90 transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
                    >
                        Sign Up
                    </button>

                    <p className="text-center text-sm text-foreground/80">
                        Already have an account?{' '}
                        <button
                            type="button"
                            onClick={onSwitchToSignIn}
                            className="font-medium text-primary hover:text-primary/80 transition-colors"
                        >
                            Sign In
                        </button>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default SignUp;