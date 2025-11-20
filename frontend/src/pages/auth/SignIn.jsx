import React, { useState } from 'react';
import { Mail, Lock, Globe } from 'lucide-react';
import AuthInput from '../../components/common/AuthInput';
import { useSigninUser } from '../../hooks/auth/useSigninUser';
import { useNavigate } from 'react-router-dom';

const SignIn = ({ onSwitchToSignUp = () => console.log('Switch to Sign Up triggered.') }) => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ email: '', password: '' });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const signinUserMutation = useSigninUser();
    const handleSubmit = (e) => {
        e.preventDefault();
        signinUserMutation.mutate(formData);
        navigate("/");
    };

    if (signinUserMutation.isLoading) return <p>Signing in...</p>;
    if (signinUserMutation.isError) return <p>Error: {signinUserMutation.error.message}</p>;

    const title = 'Sign In to ExamPro';
    const description = 'Enter your credentials to access the Exam Management System.';

    return (
        <div className="flex items-center justify-center min-h-screen bg-background p-4 sm:p-6">
            <div className="w-full max-w-lg p-6 sm:p-8 bg-card rounded-2xl shadow-2xl border border-border">

                <div className="flex flex-col items-center space-y-2 mb-8">
                    <Globe className="h-10 w-10 text-primary" />
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">{title}</h1>
                    <p className="text-sm text-foreground/70 text-center">{description}</p>
                </div>

                <form onSubmit={handleSubmit} className="w-full max-w-md space-y-6 mx-auto">
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
                        placeholder="••••••••"
                    />

                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <input
                                id="remember-me"
                                name="remember-me"
                                type="checkbox"
                                className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                            />
                            <label htmlFor="remember-me" className="ml-2 block text-sm text-foreground/80">
                                Remember me
                            </label>
                        </div>

                        <div className="text-sm">
                            <a href="#" className="font-medium text-primary hover:text-primary/80 transition-colors">
                                Forgot your password?
                            </a>
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="w-full justify-center rounded-md bg-primary py-2 px-4 text-sm font-semibold text-primary-foreground shadow-md hover:bg-primary/90 transition-colors duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
                    >
                        Sign In
                    </button>

                    <p className="text-center text-sm text-foreground/80">
                        Don't have an account?{' '}
                        <button
                            type="button"
                            onClick={onSwitchToSignUp}
                            className="font-medium text-primary hover:text-primary/80 transition-colors"
                        >
                            Sign Up
                        </button>
                    </p>
                </form>
            </div>
        </div>
    );
};

export default SignIn;