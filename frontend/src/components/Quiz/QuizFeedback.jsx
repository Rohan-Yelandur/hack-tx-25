import React from 'react';

function QuizFeedback({ correct, explanation, onNext }) {
  return (
    <div className={`quiz-feedback ${correct ? 'correct' : 'incorrect'}`}>
      <div className="quiz-feedback-icon">
        {correct ? (
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="8 12 11 15 16 9"></polyline>
          </svg>
        ) : (
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        )}
      </div>
      <div className="quiz-feedback-content">
        <h3 className="quiz-feedback-title">
          {correct ? 'Correct!' : 'Not quite right'}
        </h3>
        <p className="quiz-feedback-explanation">{explanation}</p>
      </div>
      <button onClick={onNext} className="quiz-feedback-button">
        {correct ? 'Next' : 'Try Again'}
      </button>
    </div>
  );
}

export default QuizFeedback;
