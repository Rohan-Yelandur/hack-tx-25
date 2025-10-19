import React from 'react';

function QuizResults({ score, totalQuestions, questions, userAnswers, onRetake }) {
  const percentage = Math.round((score / totalQuestions) * 100);

  const getMessage = () => {
    if (percentage >= 80) return "Excellent work! 🎉";
    if (percentage >= 60) return "Good job! 👍";
    if (percentage >= 40) return "Keep practicing! 📚";
    return "Try again! 💪";
  };

  return (
    <div className="quiz-results">
      <div className="quiz-results-header">
        <h2 className="quiz-results-title">Quiz Complete!</h2>
        <div className="quiz-results-score-display">
          <div className="quiz-results-score-circle">
            <span className="quiz-results-percentage">{percentage}%</span>
          </div>
          <p className="quiz-results-score-text">
            {score} out of {totalQuestions} correct
          </p>
          <p className="quiz-results-message">{getMessage()}</p>
        </div>
      </div>

      <div className="quiz-results-summary">
        <h3>Question Summary</h3>
        {questions.map((question, index) => {
          const isCorrect = userAnswers[question.id] !== undefined;
          return (
            <div key={question.id} className={`quiz-result-item ${isCorrect ? 'correct' : 'incorrect'}`}>
              <div className="quiz-result-item-header">
                <span className="quiz-result-item-number">Q{index + 1}</span>
                <span className="quiz-result-item-icon">
                  {isCorrect ? '✓' : '✗'}
                </span>
              </div>
              <p className="quiz-result-item-question">{question.question_text}</p>
            </div>
          );
        })}
      </div>

      <div className="quiz-results-actions">
        <button onClick={onRetake} className="quiz-retake-button">
          Retake Quiz
        </button>
      </div>
    </div>
  );
}

export default QuizResults;
