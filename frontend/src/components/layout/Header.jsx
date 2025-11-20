import React, { useEffect, useState } from 'react';
import { User, LogOut, Menu, X, Globe, Book, Trophy } from 'lucide-react';
import { useCurrentAuthenticatedUser } from '../../hooks/auth/useGetcurrentUser';
import { useNavigate } from 'react-router-dom';

const useNavigation = () => {
    const [isOpen, setIsOpen] = useState(false);
    const toggleMenu = () => setIsOpen(!isOpen);

    const navItems = [
        { name: 'About', icon: User, href: '#about' },
        { name: 'Courses', icon: Book, href: '#courses' },
        { name: 'Results', icon: Trophy, href: '#results' },
    ];

    return { isOpen, toggleMenu, navItems };
};


const Header = () => {
    const navigate = useNavigate();
    const { isOpen, toggleMenu, navItems } = useNavigation();

    const { data: user, isLoading, isError } = useCurrentAuthenticatedUser();

    useEffect(() => {
        if (isError) {
            navigate("/sign-in");
        }
    }, [isError]);

    if (isLoading) return <p>Loading user...</p>;

    const handleLogout = () => {
        console.log("User logged out.");
        window.location.href = '/';
    };

    return (
        <header className="sticky top-0 z-50 bg-card/90 backdrop-blur-md border-b border-border shadow-sm font-sans">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">

                    <a href="/" className="flex items-center space-x-2">
                        <Globe className="h-6 w-6 text-primary" />
                        <span className="text-xl font-extrabold tracking-tight text-foreground">
                            ExamPro
                        </span>
                    </a>

                    <nav className="hidden md:flex space-x-2 lg:space-x-6">
                        {navItems.map((item) => (
                            <a
                                key={item.name}
                                href={item.href}
                                className="inline-flex items-center text-sm font-medium text-foreground/80 hover:text-primary transition-colors duration-200 p-2 rounded-lg"
                            >
                                <item.icon className="h-4 w-4 mr-1.5" />
                                {item.name}
                            </a>
                        ))}
                    </nav>

                    <div className="hidden md:flex items-center space-x-3">

                        {user ? (
                            <>
                                <div className="relative group">
                                    <span className="text-sm font-medium text-foreground/80 hidden lg:inline">
                                        Welcome, <strong className="text-primary">{user.username}</strong>
                                    </span>


                                    <User className="h-8 w-8 p-1 rounded-full bg-secondary text-primary cursor-pointer hover:bg-accent transition-colors" />
                                    <div className="absolute right-0 mt-3 w-40 origin-top-right rounded-md shadow-2xl bg-card ring-1 ring-black/10 hidden group-hover:block transition-all duration-300 z-50">
                                        <div className="py-1">
                                            <a href="#profile" className="flex items-center px-4 py-2 text-sm text-foreground/80 hover:bg-secondary/50 transition-colors">
                                                <User className="h-4 w-4 mr-2" /> My Profile
                                            </a>
                                            <button
                                                onClick={handleLogout}
                                                className="flex items-center w-full px-4 py-2 text-sm text-danger hover:bg-danger/10 transition-colors"
                                            >
                                                <LogOut className="h-4 w-4 mr-2" /> Sign Out
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </>
                        ) :
                            (
                                <div className="hidden md:flex space-x-2 lg:space-x-6">
                                    <a href='/sign-up' className="inline-flex items-center text-sm font-medium text-foreground/80 hover:text-primary transition-colors duration-200 p-2 rounded-lg">
                                        Sign Up
                                    </a>

                                    <a href='/sign-in' className="inline-flex items-center text-sm font-medium text-foreground/80 hover:text-primary transition-colors duration-200 p-2 rounded-lg">
                                        Sign In
                                    </a>
                                </div>
                            )}



                    </div>

                    <button
                        className="md:hidden text-foreground hover:text-primary p-2 rounded-md transition-colors"
                        onClick={toggleMenu}
                        aria-label="Toggle navigation"
                    >
                        {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                    </button>
                </div>
            </div>

            <div
                className={`md:hidden overflow-hidden transition-all duration-300 ${isOpen ? 'max-h-96 opacity-100 py-2' : 'max-h-0 opacity-0'}`}
            >
                <div className="px-4 pt-2 pb-3 space-y-1 sm:px-6">
                    {navItems.map((item) => (
                        <a
                            key={item.name}
                            href={item.href}
                            className="flex items-center w-full px-3 py-2 rounded-md text-base font-medium text-foreground/80 hover:bg-secondary hover:text-primary transition-colors duration-200"
                            onClick={toggleMenu}
                        >
                            <item.icon className="h-5 w-5 mr-3" />
                            {item.name}
                        </a>
                    ))}
                    <button
                        onClick={() => { handleLogout(); toggleMenu(); }}
                        className="flex items-center w-full px-3 py-2 rounded-md text-base font-medium text-danger hover:bg-danger/10 transition-colors duration-200"
                    >
                        <LogOut className="h-5 w-5 mr-3" /> Sign Out
                    </button>
                </div>
            </div>
        </header>
    );
};
export default Header;