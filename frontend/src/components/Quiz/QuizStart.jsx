import React from 'react';

function QuizStart({ onStart, totalQuestions }) {
  return (
    <div className="quiz-start">
      <div className="quiz-start-content">
        <h2 className="quiz-start-title">Test Your Knowledge!</h2>
        <p className="quiz-start-description">
          Complete this quiz to reinforce what you've learned from the video.
        </p>
        <div className="quiz-start-info">
          <div className="quiz-info-item">
            <span className="quiz-info-icon">📝</span>
            <span>{totalQuestions} Questions</span>
          </div>
          <div className="quiz-info-item">
            <span className="quiz-info-icon">⭐</span>
            <span>Sequential stages</span>
          </div>
          <div className="quiz-info-item">
            <span className="quiz-info-icon">💡</span>
            <span>Hints available</span>
          </div>
        </div>
        <button onClick={onStart} className="quiz-start-button">
          Start Quiz
        </button>
      </div>
    </div>
  );
}

export default QuizStart;
