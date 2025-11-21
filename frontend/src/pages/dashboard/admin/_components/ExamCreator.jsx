import React, { useState, useMemo } from 'react';
import { Search, List, Settings, Plus, X, Calendar, Clock, CheckCircle, Save } from 'lucide-react';
import {useCreateExam} from '../../../../hooks/exam/useCreateExam';
import { useUpdateExam } from '../../../../hooks/exam/useUpdateExam';
import {useListQuestions} from "../../../../hooks/exam/useListQuestions";

const ExamCreator = ({ questions, exams, setExams }) => {
    const [isCreating, setIsCreating] = useState(false);
    const [newExam, setNewExam] = useState({ title: '', duration: 60, startTime: '', endTime: '', questionIds: [] });
    const [searchTerm, setSearchTerm] = useState('');

    const availableQuestions = useMemo(() => {
        return questions.filter(q =>
            q.text.toLowerCase().includes(searchTerm.toLowerCase()) &&
            !newExam.questionIds.includes(q.id)
        );
    }, [questions, searchTerm, newExam.questionIds]);

    const selectedQuestions = useMemo(() => {
        return questions.filter(q => newExam.questionIds.includes(q.id));
    }, [questions, newExam.questionIds]);

    const handleToggleQuestion = (id) => {
        setNewExam(prev => {
            const isSelected = prev.questionIds.includes(id);
            return {
                ...prev,
                questionIds: isSelected
                    ? prev.questionIds.filter(qId => qId !== id)
                    : [...prev.questionIds, id]
            };
        });
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewExam(prev => ({ ...prev, [name]: name === 'duration' ? parseInt(value) || 0 : value }));
    };

    const handleCreateExam = (e) => {
        e.preventDefault();
        const newExamObj = {
            ...newExam,
            id: Date.now(),
            status: 'Draft',
            totalQuestions: newExam.questionIds.length
        };
        setExams(prev => [...prev, newExamObj]);
        setNewExam({ title: '', duration: 60, startTime: '', endTime: '', questionIds: [] });
        setIsCreating(false);
        alert(`Exam "${newExamObj.title}" created successfully as a Draft.`);
    };

    const handleTogglePublish = (id) => {
        setExams(prev => prev.map(exam =>
            exam.id === id ? { ...exam, status: exam.status === 'Published' ? 'Draft' : 'Published' } : exam
        ));
    };

    const formatDate = (datetime) => {
        if (!datetime) return "N/A";
        const d = new Date(datetime);
        return d.toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' });
    }

    if (isCreating) {
        return (
            <div className="bg-card p-8 rounded-2xl shadow-xl border border-border">
                <div className="flex justify-between items-center mb-6 border-b border-border pb-4">
                    <h2 className="text-2xl font-bold text-primary flex items-center"><Plus className="h-6 w-6 mr-3" /> Create New Exam</h2>
                    <button onClick={() => setIsCreating(false)} className="bg-secondary text-foreground font-semibold px-4 py-2 rounded-xl hover:bg-accent transition-colors">
                        <List className="h-4 w-4 mr-2" /> Back to List
                    </button>
                </div>

                <form onSubmit={handleCreateExam} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 bg-secondary/30 p-4 rounded-xl">
                        <div>
                            <label className="text-sm font-semibold text-foreground/80 block mb-1">Exam Title</label>
                            <input name="title" value={newExam.title} onChange={handleInputChange} required className="w-full p-2 rounded-lg border border-input bg-card" />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-foreground/80 block mb-1">Duration (Minutes)</label>
                            <input name="duration" type="number" value={newExam.duration} onChange={handleInputChange} required className="w-full p-2 rounded-lg border border-input bg-card" />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-foreground/80 block mb-1">Start Time</label>
                            <input name="startTime" type="datetime-local" value={newExam.startTime} onChange={handleInputChange} required className="w-full p-2 rounded-lg border border-input bg-card" />
                        </div>
                        <div>
                            <label className="text-sm font-semibold text-foreground/80 block mb-1">End Time</label>
                            <input name="endTime" type="datetime-local" value={newExam.endTime} onChange={handleInputChange} required className="w-full p-2 rounded-lg border border-input bg-card" />
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <div className="border border-border rounded-xl p-4 bg-primary/5">
                            <h3 className="font-bold text-lg text-primary mb-3 flex items-center"><CheckCircle className="h-5 w-5 mr-2" /> Selected Questions ({selectedQuestions.length})</h3>
                            <ul className="space-y-2 max-h-80 overflow-y-auto pr-2">
                                {selectedQuestions.length === 0 ? (
                                    <li className="text-sm text-foreground/60 p-2">Select questions from the bank below.</li>
                                ) : (
                                    selectedQuestions.map(q => (
                                        <li key={q.id} className="flex justify-between items-center bg-card p-3 rounded-lg shadow-sm border border-primary/20">
                                            <span className="text-sm truncate">{q.text}</span>
                                            <button type="button" onClick={() => handleToggleQuestion(q.id)} className="text-danger hover:text-danger/70 transition-colors p-1">
                                                <X className="h-4 w-4" />
                                            </button>
                                        </li>
                                    ))
                                )}
                            </ul>
                            <p className="mt-3 font-semibold text-foreground/80">Total Questions: {selectedQuestions.length}</p>
                        </div>

                        <div>
                            <h3 className="font-bold text-lg text-foreground mb-3 flex items-center"><List className="h-5 w-5 mr-2" /> Question Bank</h3>
                            <div className="relative mb-3">
                                <Search className="h-4 w-4 text-foreground/50 absolute left-3 top-1/2 transform -translate-y-1/2" />
                                <input
                                    type="text"
                                    placeholder="Search question to add..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 rounded-lg border border-input bg-secondary"
                                />
                            </div>
                            <ul className="space-y-2 max-h-80 overflow-y-auto pr-2 border border-border rounded-lg p-2">
                                {availableQuestions.length === 0 ? (
                                    <li className="text-sm text-foreground/60 p-2">No unselected questions match your search.</li>
                                ) : (
                                    availableQuestions.map(q => (
                                        <li key={q.id} className="flex justify-between items-center bg-secondary p-3 rounded-lg hover:bg-secondary/70 transition-colors">
                                            <span className="text-sm truncate">{q.text}</span>
                                            <button type="button" onClick={() => handleToggleQuestion(q.id)} className="bg-primary text-primary-foreground text-xs font-bold px-3 py-1 rounded-full hover:bg-primary/90 transition-colors">
                                                Add
                                            </button>
                                        </li>
                                    ))
                                )}
                            </ul>
                        </div>
                    </div>

                    <button type="submit" disabled={selectedQuestions.length === 0} className="w-full bg-primary text-primary-foreground font-semibold px-6 py-3 rounded-xl hover:bg-primary/90 transition-colors flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed">
                        <Save className="h-5 w-5 mr-3" /> Save Exam as Draft
                    </button>
                </form>
            </div>
        );
    }

    return (
        <div className="bg-card p-6 rounded-2xl shadow-xl border border-border space-y-6">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-foreground flex items-center"><Settings className="h-6 w-6 mr-3 text-primary" /> Manage Exams ({exams.length})</h2>
                <button onClick={() => setIsCreating(true)} className="bg-success text-success-foreground font-semibold px-4 py-2 rounded-xl hover:bg-success/90 transition-colors flex items-center">
                    <Plus className="h-5 w-5 mr-2" /> New Exam
                </button>
            </div>

            {/* Exam List Table */}
            <div className="overflow-x-auto border border-border rounded-xl shadow-inner">
                <table className="min-w-full divide-y divide-border">
                    <thead className="bg-secondary">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Title</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Questions</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Time Window</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase">Duration</th>
                            <th className="px-6 py-3 text-center text-xs font-medium text-foreground/80 uppercase">Status</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-foreground/80 uppercase">Publish/Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-card divide-y divide-border">
                        {exams.length === 0 ? (
                            <tr><td colSpan="6" className="py-8 text-center text-foreground/60">No exams have been created yet.</td></tr>
                        ) : (
                            exams.map(exam => (
                                <tr key={exam.id} className="hover:bg-secondary/50 transition-colors">
                                    <td className="px-6 py-4 font-semibold text-sm text-foreground">{exam.title}</td>
                                    <td className="px-6 py-4 text-sm text-foreground/70">{exam.totalQuestions}</td>
                                    <td className="px-6 py-4 text-xs text-foreground/70 space-y-1">
                                        <div className="flex items-center"><Calendar className="h-4 w-4 mr-1 text-primary" /> {formatDate(exam.startTime)}</div>
                                        <div className="flex items-center"><Clock className="h-4 w-4 mr-1 text-danger" /> {formatDate(exam.endTime)}</div>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-foreground/70">{exam.duration} mins</td>
                                    <td className="px-6 py-4 text-center">
                                        <span className={`px-3 py-1 text-xs font-semibold rounded-full ${exam.status === 'Published' ? 'bg-success/20 text-success' : 'bg-warning/20 text-warning'}`}>
                                            {exam.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-right whitespace-nowrap">
                                        <button
                                            onClick={() => handleTogglePublish(exam.id)}
                                            className={`font-semibold px-4 py-2 rounded-xl transition-colors text-sm ${exam.status === 'Published' ? 'bg-danger/10 text-danger hover:bg-danger/20' : 'bg-success/10 text-success hover:bg-success/20'}`}
                                        >
                                            {exam.status === 'Published' ? 'Unpublish' : 'Publish'}
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ExamCreator