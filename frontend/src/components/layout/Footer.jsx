import React, { useState } from 'react';
import { Mail, FileText, Globe } from 'lucide-react';


const Footer = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-[hsl(222,47%,11%)] text-white mt-10">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 border-t border-border/20 pt-8">

                    <div className="space-y-3">
                        <h3 className="text-xl font-extrabold text-primary">ExamPro</h3>
                        <p className="text-sm text-secondary-foreground/80 max-w-xs">
                            Empowering students and educators with secure, efficient, and flexible online examination tools.
                        </p>
                    </div>

                    <div className="space-y-3">
                        <h4 className="text-lg font-semibold mb-2 text-white">Legal & Support</h4>
                        <ul className="space-y-2">
                            <li className="flex items-center">
                                <FileText className="h-4 w-4 mr-2 text-primary" />
                                <a href="#terms" className="text-sm hover:text-primary transition-colors">Terms of Service</a>
                            </li>
                            <li className="flex items-center">
                                <FileText className="h-4 w-4 mr-2 text-primary" />
                                <a href="#privacy" className="text-sm hover:text-primary transition-colors">Privacy Policy</a>
                            </li>
                        </ul>
                    </div>

                    <div className="space-y-3">
                        <h4 className="text-lg font-semibold mb-2 text-white">Get in Touch</h4>
                        <ul className="space-y-2">
                            <li className="flex items-center">
                                <Mail className="h-4 w-4 mr-2 text-primary" />
                                <a href="mailto:support@exampro.com" className="text-sm hover:text-primary transition-colors">support@exampro.com</a>
                            </li>
                            <li className="flex items-center">
                                <Globe className="h-4 w-4 mr-2 text-primary" />
                                <span className="text-sm">Global Headquarters, 123 Exam Lane</span>
                            </li>
                        </ul>
                    </div>

                </div>

                <div className="mt-10 pt-4 border-t border-border/20 text-center">
                    <p className="text-xs text-secondary-foreground/60">
                        &copy; {currentYear} ExamPro. All rights reserved.
                    </p>
                </div>
            </div>
        </footer>
    );
};
export default Footer;