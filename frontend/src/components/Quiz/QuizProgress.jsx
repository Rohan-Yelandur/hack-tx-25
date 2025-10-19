import React from 'react';

function QuizProgress({ currentQuestion, totalQuestions, score }) {
  const percentage = ((currentQuestion - 1) / totalQuestions) * 100;

  return (
    <div className="quiz-progress">
      <div className="quiz-progress-header">
        <span className="quiz-progress-text">
          Question {currentQuestion} of {totalQuestions}
        </span>
        <span className="quiz-score">
          Score: {score}/{totalQuestions}
        </span>
      </div>
      <div className="quiz-progress-bar">
        <div
          className="quiz-progress-fill"
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
}

export default QuizProgress;
