import React, { useState, useMemo } from 'react';
import { Search, List, Eye, Trash2 } from 'lucide-react';
import QuestionDetailModal from './QuestionDetailModal';

const QuestionBank = ({ questions, setQuestions }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [filterSubject, setFilterSubject] = useState('All');
    const [selectedQuestion, setSelectedQuestion] = useState(null);

    const availableSubjects = useMemo(() => [
        'All', ...new Set(questions.map(q => q.subject))
    ], [questions]);

    const filteredQuestions = useMemo(() => {
        return questions.filter(q => {
            const matchesSearch = q.text.toLowerCase().includes(searchTerm.toLowerCase());
            const matchesSubject = filterSubject === 'All' || q.subject === filterSubject;
            return matchesSearch && matchesSubject;
        });
    }, [questions, searchTerm, filterSubject]);

    const handleDelete = (id) => {
        if (window.confirm(`Are you sure you want to delete Question #${id}? This action cannot be undone.`)) {
            setQuestions(questions.filter(q => q.id !== id));
        }
    }

    return (
        <div className="bg-card p-6 rounded-2xl shadow-xl border border-border space-y-6">
            <h2 className="text-2xl font-bold text-foreground flex items-center"><List className="h-6 w-6 mr-3 text-primary" /> Question Bank ({questions.length})</h2>

            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
                <div className="relative">
                    <Search className="h-5 w-5 text-foreground/50 absolute left-3 top-1/2 transform -translate-y-1/2" />
                    <input
                        type="text"
                        placeholder="Search question text or tags..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-10 pr-4 py-2 rounded-xl border border-input bg-secondary focus:ring-2 focus:ring-primary focus:border-primary transition-all"
                    />
                </div>
                <select
                    value={filterSubject}
                    onChange={(e) => setFilterSubject(e.target.value)}
                    className="py-2 px-4 rounded-xl border border-input bg-secondary text-foreground focus:ring-2 focus:ring-primary focus:border-primary transition-all w-full md:w-auto"
                >
                    {availableSubjects.map(subject => (
                        <option key={subject} value={subject}>{subject} Subjects</option>
                    ))}
                </select>
            </div>

            <div className="overflow-x-auto border border-border rounded-xl shadow-inner">
                <table className="min-w-full divide-y divide-border">
                    <thead className="bg-secondary">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Question Snippet</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Subject</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Type</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-foreground/80 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-card divide-y divide-border">
                        {filteredQuestions.length === 0 ? (
                            <tr><td colSpan="5" className="py-8 text-center text-foreground/60">No questions found matching your criteria.</td></tr>
                        ) : (
                            filteredQuestions.map(q => (
                                <tr key={q.id} className="hover:bg-secondary/50 transition-colors">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-primary">{q.id}</td>
                                    <td className="px-6 py-4 max-w-sm truncate text-sm text-foreground">{q.text}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground/70">{q.subject}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground/70">{q.type}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button
                                            onClick={() => setSelectedQuestion(q)}
                                            className="text-primary hover:text-primary/70 p-2 rounded-lg transition-colors mr-2"
                                            title="View Details"
                                        >
                                            <Eye className="h-5 w-5" />
                                        </button>
                                        <button
                                            onClick={() => handleDelete(q.id)}
                                            className="text-danger hover:text-danger/70 p-2 rounded-lg transition-colors"
                                            title="Delete Question"
                                        >
                                            <Trash2 className="h-5 w-5" />
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            <QuestionDetailModal question={selectedQuestion} onClose={() => setSelectedQuestion(null)} />
        </div>
    );
};

export default QuestionBank