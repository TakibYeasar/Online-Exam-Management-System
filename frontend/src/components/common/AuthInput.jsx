import React from 'react';

const AuthInput = ({ id, label, type, icon: Icon, value, onChange, placeholder }) => (
    <div className="space-y-2">
        <label htmlFor={id} className="text-sm font-medium text-foreground/90">
            {label}
        </label>
        <div className="relative">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <Icon className="h-4 w-4 text-primary" />
            </div>
            <input
                id={id}
                name={id}
                type={type}
                required
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                className="flex h-10 w-full rounded-md border border-input bg-secondary px-3 py-2 pl-10 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-foreground/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-shadow duration-150"
            />
        </div>
    </div>
);
export default AuthInput;