import React from 'react';
import { Award, CheckCircle, Clock } from 'lucide-react';

const Hero = () => {
    return (
        <section className="py-20 md:py-32 bg-background">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">

                <p className="text-sm font-semibold uppercase tracking-widest text-primary mb-3">
                    The Future of Secure Testing
                </p>

                <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter text-foreground mb-6">
                    Streamline Your <span className="text-primary block md:inline-block">Online Exam Management</span>
                </h1>

                <p className="max-w-3xl mx-auto text-xl text-foreground/70 mb-10">
                    ExamPro provides a robust, secure, and intuitive platform for creating, conducting, and analyzing high-stakes digital examinations for education and certification.
                </p>

                {/* Primary CTA Buttons */}
                <div className="flex justify-center space-x-4">
                    <button className="bg-primary text-primary-foreground font-semibold px-8 py-3 rounded-xl shadow-lg hover:bg-primary/90 transition-all duration-300 transform hover:scale-[1.02] ring-4 ring-primary/50">
                        Start Your Free Trial
                    </button>
                    <a
                        href="#features"
                        className="border border-input text-foreground font-medium px-8 py-3 rounded-xl hover:bg-secondary transition-colors duration-300"
                    >
                        Explore Features
                    </a>
                </div>

                {/* Trust/Key Metrics */}
                <div className="mt-16 flex justify-center space-x-12 flex-wrap text-foreground/80">
                    <div className="flex items-center space-x-2 m-2">
                        <CheckCircle className="h-5 w-5 text-success" />
                        <span className="font-medium">100% Secure Proctoring</span>
                    </div>
                    <div className="flex items-center space-x-2 m-2">
                        <Clock className="h-5 w-5 text-warning" />
                        <span className="font-medium">Instant Grading & Feedback</span>
                    </div>
                    <div className="flex items-center space-x-2 m-2">
                        <Award className="h-5 w-5 text-primary" />
                        <span className="font-medium">Trusted by 500+ Institutions</span>
                    </div>
                </div>

            </div>
        </section>
    );
};

export default Hero;