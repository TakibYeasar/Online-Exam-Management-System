import React, { useState } from 'react';
import { UploadCloud, Check, Eye } from 'lucide-react';

const QuestionImporter = ({ onImportConfirm, navigate }) => {
    const [file, setFile] = useState(null);
    const [previewData, setPreviewData] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setPreviewData(null);
    };

    const handleParse = () => {
        if (!file) return;
        setLoading(true);
        setTimeout(() => {
            const mockedRows = [
                { 'Question Text': 'Who invented the telephone?', 'Subject': 'History', 'Type': 'MCQ', 'Option A': 'Edison', 'Option B': 'Bell (Correct)', 'Option C': 'Tesla', 'Complexity': 'Easy' },
                { 'Question Text': 'What is the largest planet in our solar system?', 'Subject': 'Astronomy', 'Type': 'MCQ', 'Option A': 'Saturn', 'Option B': 'Jupiter (Correct)', 'Option C': 'Mars', 'Complexity': 'Medium' },
            ];
            setPreviewData(mockedRows);
            setLoading(false);
        }, 1500);
    };

    const handleConfirm = () => {
        onImportConfirm(previewData);
        setFile(null);
        setPreviewData(null);
        alert("Success: Questions imported and added to Question Bank.");
        navigate('questions');
    };

    return (
        <div className="bg-card p-6 rounded-2xl shadow-xl border border-border">
            <h2 className="text-2xl font-bold text-foreground mb-6 flex items-center"><UploadCloud className="h-6 w-6 mr-3 text-primary" /> Import Question Bank</h2>

            <div className="space-y-6">
                <div className="p-4 border-2 border-dashed border-border rounded-xl flex items-center justify-between bg-secondary/30">
                    <input
                        type="file"
                        accept=".xlsx, .xls, .csv"
                        onChange={handleFileChange}
                        className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary/10 file:text-primary hover:file:bg-primary/20 transition-colors cursor-pointer"
                    />
                    <button
                        onClick={handleParse}
                        disabled={!file || loading}
                        className="bg-primary text-primary-foreground font-semibold px-6 py-2 rounded-xl hover:bg-primary/90 disabled:bg-primary/50 transition-colors flex items-center"
                    >
                        {loading ? 'Parsing...' : 'Preview Data'}
                        {!loading && <Eye className="h-4 w-4 ml-2" />}
                    </button>
                </div>

                {previewData && (
                    <div className="mt-8">
                        <h3 className="text-xl font-semibold mb-3 text-foreground">Preview ({previewData.length} Rows Parsed)</h3>
                        <div className="overflow-x-auto border border-border rounded-xl shadow-inner">
                            <table className="min-w-full divide-y divide-border">
                                <thead className="bg-secondary">
                                    <tr>
                                        {Object.keys(previewData[0]).map(key => (
                                            <th key={key} className="px-6 py-3 text-left text-xs font-medium text-foreground/80 uppercase tracking-wider">{key}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody className="bg-card divide-y divide-border">
                                    {previewData.map((row, index) => (
                                        <tr key={index} className="hover:bg-secondary/50 transition-colors">
                                            {Object.values(row).map((value, i) => (
                                                <td key={i} className="px-6 py-4 whitespace-nowrap text-sm text-foreground/70 max-w-xs truncate">{value}</td>
                                            ))}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        <button
                            onClick={handleConfirm}
                            className="mt-6 w-full bg-success text-success-foreground font-semibold px-6 py-3 rounded-xl hover:bg-success/90 transition-colors flex items-center justify-center shadow-lg"
                        >
                            <Check className="h-5 w-5 mr-3" /> Confirm & Import {previewData.length} Questions
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default QuestionImporter