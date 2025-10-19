import { createContext, useContext, useState } from 'react';

const LessonContext = createContext();

export const useLessonContext = () => {
  const context = useContext(LessonContext);
  if (!context) {
    throw new Error('useLessonContext must be used within a LessonProvider');
  }
  return context;
};

export const LessonProvider = ({ children }) => {
  const [currentLesson, setCurrentLesson] = useState({
    prompt: '',
    videoUrl: '',
    narrationScript: '',
    videoId: '',
    sharedToCommunity: false,
    hasContent: false,
    loading: false,
  });

  const updateLesson = (lessonData) => {
    setCurrentLesson(prev => ({
      ...prev,
      ...lessonData,
      hasContent: true,
    }));
  };

  const clearLesson = () => {
    setCurrentLesson({
      prompt: '',
      videoUrl: '',
      narrationScript: '',
      videoId: '',
      sharedToCommunity: false,
      hasContent: false,
      loading: false,
    });
  };

  const setLoading = (isLoading) => {
    setCurrentLesson(prev => ({
      ...prev,
      loading: isLoading,
    }));
  };

  return (
    <LessonContext.Provider value={{ currentLesson, updateLesson, clearLesson, setLoading }}>
      {children}
    </LessonContext.Provider>
  );
};
