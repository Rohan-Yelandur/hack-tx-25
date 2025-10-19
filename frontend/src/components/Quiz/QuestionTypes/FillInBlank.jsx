import React, { useState } from 'react';

function FillInBlank({ question, onSubmit, disabled }) {
  const [answer, setAnswer] = useState('');

  const handleSubmit = () => {
    if (answer.trim()) {
      onSubmit(answer.trim());
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && answer.trim() && !disabled) {
      handleSubmit();
    }
  };

  return (
    <div className="question-container">
      <h3 className="question-text">{question.question_text}</h3>
      <div className="question-type-badge">Fill in the Blank</div>

      <p className="fill-in-blank-hint">
        💡 Type your answer in lowercase (synonyms may be accepted). Be precise!
      </p>

      <div className="fill-in-blank-input-wrapper">
        <input
          type="text"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your answer here..."
          disabled={disabled}
          className="fill-in-blank-input"
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={!answer.trim() || disabled}
        className="question-submit-button"
      >
        Submit Answer
      </button>
    </div>
  );
}

export default FillInBlank;
