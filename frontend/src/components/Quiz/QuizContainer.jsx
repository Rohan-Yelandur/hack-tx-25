import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../../config/constants';
import QuizStart from './QuizStart';
import QuizProgress from './QuizProgress';
import QuizFeedback from './QuizFeedback';
import QuizResults from './QuizResults';
import { MultipleChoice, FillInBlank, StepByStep } from './QuestionTypes';
import './Quiz.css';

function QuizContainer({ quizData, quizId }) {
  const [quizState, setQuizState] = useState('start'); // 'start', 'active', 'feedback', 'complete'
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [currentStage, setCurrentStage] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [score, setScore] = useState(0);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackData, setFeedbackData] = useState({ correct: false, explanation: '' });
  const [completedStages, setCompletedStages] = useState({});

  const questions = quizData?.questions || [];
  const currentQuestion = questions[currentQuestionIndex];
  const totalQuestions = questions.length;

  const startQuiz = () => {
    setQuizState('active');
    setCurrentQuestionIndex(0);
    setCurrentStage(0);
    setUserAnswers({});
    setScore(0);
    setCompletedStages({});
  };

  const validateAnswer = async (answer) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/quiz/validate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          quiz_id: quizId,
          question_id: currentQuestion.id,
          stage_number: currentQuestion.type === 'step-by-step' ? currentStage + 1 : undefined,
          user_answer: answer,
        }),
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Validation error:', error);
      return { correct: false, explanation: 'Error validating answer' };
    }
  };

  const handleAnswer = async (answer) => {
    const validation = await validateAnswer(answer);

    setFeedbackData(validation);
    setShowFeedback(true);

    if (validation.correct) {
      // Update score
      if (currentQuestion.type === 'step-by-step') {
        // For step-by-step, only count score when all stages complete
        const totalStages = currentQuestion.stages.length;
        if (currentStage === totalStages - 1) {
          setScore(score + 1);
        }

        // Mark stage as completed
        const questionKey = `q${currentQuestion.id}`;
        setCompletedStages({
          ...completedStages,
          [questionKey]: [...(completedStages[questionKey] || []), currentStage]
        });
      } else {
        setScore(score + 1);
      }

      // Store user answer
      const answerKey = currentQuestion.type === 'step-by-step'
        ? `${currentQuestion.id}_stage_${currentStage}`
        : currentQuestion.id;
      setUserAnswers({
        ...userAnswers,
        [answerKey]: answer
      });
    }
  };

  const handleNext = () => {
    setShowFeedback(false);

    // If answer was incorrect, just hide feedback and allow retry
    if (!feedbackData.correct) {
      return;
    }

    // Answer was correct, proceed to next stage or question
    if (currentQuestion.type === 'step-by-step') {
      const totalStages = currentQuestion.stages.length;

      if (currentStage < totalStages - 1) {
        // Move to next stage
        setCurrentStage(currentStage + 1);
        return;
      }
    }

    // Move to next question or finish
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentStage(0);
    } else {
      setQuizState('complete');
    }
  };

  const retakeQuiz = () => {
    startQuiz();
  };

  const renderQuestion = () => {
    if (!currentQuestion) return null;

    const questionProps = {
      question: currentQuestion,
      onSubmit: handleAnswer,
      disabled: showFeedback,
    };

    switch (currentQuestion.type) {
      case 'multiple-choice':
        return <MultipleChoice {...questionProps} />;
      case 'fill-in-blank':
        return <FillInBlank {...questionProps} />;
      case 'step-by-step':
        return (
          <StepByStep
            {...questionProps}
            currentStage={currentStage}
            completedStages={completedStages[`q${currentQuestion.id}`] || []}
            userAnswers={userAnswers}
          />
        );
      default:
        return <div>Unknown question type</div>;
    }
  };

  if (quizState === 'start') {
    return <QuizStart onStart={startQuiz} totalQuestions={totalQuestions} />;
  }

  if (quizState === 'complete') {
    return (
      <QuizResults
        score={score}
        totalQuestions={totalQuestions}
        questions={questions}
        userAnswers={userAnswers}
        onRetake={retakeQuiz}
      />
    );
  }

  return (
    <div className="quiz-container">
      <QuizProgress
        currentQuestion={currentQuestionIndex + 1}
        totalQuestions={totalQuestions}
        score={score}
      />

      <div className="quiz-question-area">
        {renderQuestion()}
      </div>

      {showFeedback && (
        <QuizFeedback
          correct={feedbackData.correct}
          explanation={feedbackData.explanation}
          onNext={handleNext}
        />
      )}
    </div>
  );
}

export default QuizContainer;
