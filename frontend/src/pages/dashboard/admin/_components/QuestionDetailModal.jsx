import React from 'react';
import {CheckCircle} from 'lucide-react';

const QuestionDetailModal = ({ question, onClose }) => {
    if (!question) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50 p-4">
            <div className="bg-card rounded-2xl w-full max-w-2xl shadow-2xl border border-border">
                <div className="flex justify-between items-center p-6 border-b border-border">
                    <h3 className="text-2xl font-bold text-primary">Question #{question.id} Details</h3>
                    <button onClick={onClose} className="p-2 rounded-full text-foreground hover:bg-secondary transition-colors">
                        <X className="h-5 w-5" />
                    </button>
                </div>

                <div className="p-6 space-y-4">
                    <div className="flex justify-between text-sm text-foreground/80">
                        <span><strong className="font-semibold">Subject:</strong> {question.subject}</span>
                        <span><strong className="font-semibold">Type:</strong> {question.type}</span>
                        <span><strong className="font-semibold">Complexity:</strong> <span className={`font-bold ${question.complexity === 'Hard' ? 'text-danger' : question.complexity === 'Medium' ? 'text-warning' : 'text-success'}`}>{question.complexity}</span></span>
                    </div>

                    <div className="bg-secondary p-4 rounded-lg">
                        <p className="font-semibold text-foreground mb-2">Question:</p>
                        <p className="text-lg">{question.text}</p>
                    </div>

                    {question.options.length > 0 && (
                        <div>
                            <p className="font-semibold text-foreground mb-2">Options:</p>
                            <ul className="space-y-2">
                                {question.options.map((option, index) => (
                                    <li key={index} className={`flex items-start p-3 rounded-lg border ${option.correct ? 'bg-success/10 border-success' : 'bg-card border-border'}`}>
                                        <CheckCircle className={`h-5 w-5 mr-3 mt-0.5 ${option.correct ? 'text-success' : 'text-foreground/50'}`} />
                                        <span className={`${option.correct ? 'font-bold text-success' : 'text-foreground'}`}>
                                            ({option.id.toUpperCase()}) {option.text}
                                        </span>
                                    </li>
                                ))}
                            </ul>
                            <p className="mt-4 text-sm text-foreground/80">
                                <strong className="font-semibold">Correct Answer Key:</strong> <span className="text-success font-bold">{question.answer.toUpperCase()}</span>
                            </p>
                        </div>
                    )}
                    {question.type === 'Essay' && (
                        <div className="p-4 bg-primary/10 rounded-lg text-primary">
                            <p className="font-semibold">Expected Answer: </p>
                            <p className="italic text-sm">Requires manual grading.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default QuestionDetailModal