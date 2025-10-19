import React from 'react';

function QuizStart({ onStart, totalQuestions }) {
  return (
    <div className="quiz-start">
      <div className="quiz-start-content">
        <h2 className="quiz-start-title">Test Your Knowledge!</h2>
        <p className="quiz-start-description">
          Complete this quiz to practice the concepts from the video.
        </p>
        <div className="quiz-start-info">
          <div className="quiz-info-item">
            <span>{totalQuestions} Questions</span>
          </div>
          <div className="quiz-info-item">
            <span>Sequential stages</span>
          </div>
          <div className="quiz-info-item">
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
