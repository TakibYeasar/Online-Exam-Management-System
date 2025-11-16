import React from 'react';
import { Zap, Shield, BarChart, HardHat, FileEdit, Clock } from 'lucide-react';

const featureList = [
    {
        icon: Shield,
        title: 'Advanced Proctoring',
        description: 'Ensure integrity with AI-powered monitoring, browser lockdown, and biometric verification.',
    },
    {
        icon: Zap,
        title: 'Lightning-Fast Grading',
        description: 'Automatic grading for multiple choice, fill-in-the-blank, and matching questions. Instant results delivery.',
    },
    {
        icon: BarChart,
        title: 'In-Depth Analytics',
        description: 'Access detailed performance reports, question difficulty indices, and student progress tracking.',
    },
    {
        icon: HardHat,
        title: 'Custom Exam Builder',
        description: 'Drag-and-drop interface for creating complex tests, question banks, and randomized paper generation.',
    },
    {
        icon: FileEdit,
        title: 'Flexible Question Types',
        description: 'Support for essay, coding challenges, multimedia integration, and complex mathematical formulas.',
    },
    {
        icon: Clock,
        title: 'Scheduled & On-Demand',
        description: 'Run exams at fixed times globally or allow students to start on demand within a defined window.',
    },
];

const Features = () => {
    return (
        <section id="features" className="py-20 bg-secondary/30">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold tracking-tight text-foreground mb-4">
                        Built for Scale, Powered by Security
                    </h2>
                    <p className="text-lg text-foreground/70 max-w-2xl mx-auto">
                        Everything you need to move your high-stakes exams online, flawlessly.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {featureList.map((feature, index) => (
                        <div
                            key={index}
                            className="bg-card p-6 rounded-xl shadow-lg border border-border transition-transform duration-300 hover:shadow-xl hover:scale-[1.01] flex flex-col items-start"
                        >
                            <feature.icon className="h-8 w-8 text-primary mb-4 p-1.5 rounded-full bg-primary/10" />
                            <h3 className="text-xl font-semibold text-foreground mb-2">
                                {feature.title}
                            </h3>
                            <p className="text-foreground/70 text-sm">
                                {feature.description}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Features;