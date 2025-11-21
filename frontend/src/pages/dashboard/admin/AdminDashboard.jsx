import React, { use, useState } from 'react';
import { UploadCloud, List, Settings, Lock } from 'lucide-react';
import QuestionBank from './_components/QuestionBank';
import ExamCreator from './_components/ExamCreator';
import QuestionImporter from './_components/QuestionImporter';
import { useAvailableExams } from '../../../hooks/exam/useAvailableExams';
import { useListQuestions } from '../../../hooks/exam/useListQuestions';


const AdminDashboard = () => {
  const [currentView, setCurrentView] = useState('questions');

  const { data: examsData } = useAvailableExams();
  const exams = examsData || [];

  const { data: questionsData, refetch: refetchQuestions } = useListQuestions({});
  const questions = questionsData || [];

  const navItems = [
    { id: 'questions', name: 'Question Bank', icon: List, component: QuestionBank, count: questions.length },
    { id: 'exams', name: 'Exam Management', icon: Settings, component: ExamCreator, count: exams.length },
    { id: 'import', name: 'Import Questions', icon: UploadCloud, component: QuestionImporter },
  ];

  const CurrentComponent = navItems.find(item => item.id === currentView)?.component;

  return (
    <div className="flex flex-col min-h-screen bg-background font-sans">
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-10">

        <header className="mb-8">
          <h1 className="text-4xl font-extrabold tracking-tight text-foreground flex items-center">
            <Lock className="h-8 w-8 mr-4 text-primary" />
            Admin Console
          </h1>
          <p className="text-lg text-foreground/70 mt-1">Manage all system content, users, and examination schedules.</p>
        </header>

        <nav className="flex space-x-2 lg:space-x-4 border-b border-border mb-8 overflow-x-auto pb-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`flex items-center px-4 py-2 rounded-t-xl font-semibold text-sm transition-colors duration-200 ${currentView === item.id
                ? 'bg-card text-primary border-b-2 border-primary shadow-inner'
                : 'text-foreground/70 hover:text-primary/80 hover:bg-secondary/50'
                }`}
            >
              <item.icon className="h-5 w-5 mr-2" />
              {item.name}
              {item.count !== undefined && (
                <span className={`ml-2 text-xs font-bold px-2 py-0.5 rounded-full ${currentView === item.id ? 'bg-primary text-primary-foreground' : 'bg-secondary text-foreground'}`}>
                  {item.count}
                </span>
              )}
            </button>
          ))}
        </nav>

        <div className="min-h-[60vh]">
          {CurrentComponent && (
            <CurrentComponent
              questions={questions}
              setQuestions={questions}
              exams={exams}
              setExams={exams}
              navigate={setCurrentView}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard