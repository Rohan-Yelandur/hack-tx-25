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
    // Quiz data
    quizData: null,
    quizId: null,
    // Loading states
    videoLoading: false,
    quizLoading: false,
  });

  const updateLesson = (lessonData) => {
    setCurrentLesson(prev => ({
      ...prev,
      ...lessonData,
      hasContent: !!(lessonData.videoUrl || prev.videoUrl),
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
      quizData: null,
      quizId: null,
      videoLoading: false,
      quizLoading: false,
    });
  };

  const setLoading = (isLoading) => {
    setCurrentLesson(prev => ({
      ...prev,
      loading: isLoading,
    }));
  };

  const setVideoLoading = (isLoading) => {
    setCurrentLesson(prev => ({
      ...prev,
      videoLoading: isLoading,
    }));
  };

  const setQuizLoading = (isLoading) => {
    setCurrentLesson(prev => ({
      ...prev,
      quizLoading: isLoading,
    }));
  };

  return (
    <LessonContext.Provider value={{
      currentLesson,
      updateLesson,
      clearLesson,
      setLoading,
      setVideoLoading,
      setQuizLoading,
    }}>
      {children}
    </LessonContext.Provider>
  );
};
