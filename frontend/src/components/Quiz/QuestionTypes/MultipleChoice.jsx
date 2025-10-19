import React, { useState } from 'react';

function MultipleChoice({ question, onSubmit, disabled }) {
  const [selectedOption, setSelectedOption] = useState('');

  const handleSubmit = () => {
    if (selectedOption) {
      onSubmit(selectedOption);
    }
  };

  return (
    <div className="question-container">
      <h3 className="question-text">{question.question_text}</h3>
      <div className="question-type-badge">Multiple Choice</div>

      <div className="multiple-choice-options">
        {question.options.map((option, index) => (
          <button
            key={index}
            className={`multiple-choice-option ${selectedOption === option ? 'selected' : ''}`}
            onClick={() => !disabled && setSelectedOption(option)}
            disabled={disabled}
          >
            <span className="option-letter">{String.fromCharCode(65 + index)}</span>
            <span className="option-text">{option}</span>
          </button>
        ))}
      </div>

      <button
        onClick={handleSubmit}
        disabled={!selectedOption || disabled}
        className="question-submit-button"
      >
        Submit Answer
      </button>
    </div>
  );
}

export default MultipleChoice;
