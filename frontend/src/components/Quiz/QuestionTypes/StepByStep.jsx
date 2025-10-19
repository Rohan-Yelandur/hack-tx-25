import React, { useState } from 'react';

function StepByStep({ question, currentStage, completedStages, userAnswers, onSubmit, disabled }) {
  const [answer, setAnswer] = useState('');
  const [showHint, setShowHint] = useState(false);

  const stages = question.stages || [];
  const activeStage = stages[currentStage];

  const handleSubmit = () => {
    if (answer.trim()) {
      onSubmit(answer.trim());
      setAnswer('');
      setShowHint(false);
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
      <div className="question-type-badge">Step-by-Step</div>

      <div className="step-by-step-stages">
        {stages.map((stage, index) => {
          const isCompleted = completedStages.includes(index);
          const isCurrent = index === currentStage;
          const isFuture = index > currentStage;

          return (
            <div
              key={index}
              className={`stage-item ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isFuture ? 'future' : ''}`}
            >
              <div className="stage-header">
                <div className="stage-number">
                  {isCompleted ? (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  ) : (
                    <span>{index + 1}</span>
                  )}
                </div>
                <span className="stage-title">Step {index + 1}</span>
              </div>

              {isCompleted && (
                <div className="stage-completed-content">
                  <p className="stage-prompt">{stage.prompt}</p>
                  <div className="stage-answer">
                    <span className="stage-answer-label">Your answer:</span>
                    <span className="stage-answer-value">
                      {userAnswers[`${question.id}_stage_${index}`]}
                    </span>
                  </div>
                </div>
              )}

              {isCurrent && (
                <div className="stage-current-content">
                  <p className="stage-prompt">{stage.prompt}</p>
                  <p className="stage-format-hint">
                    💡 Enter your answer exactly as it appears (e.g., "2x = 8" or "x = 4").
                    Be precise with spacing and formatting.
                  </p>
                  <div className="stage-input-wrapper">
                    <input
                      type="text"
                      value={answer}
                      onChange={(e) => setAnswer(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Type your answer..."
                      disabled={disabled}
                      className="stage-input"
                      autoFocus
                    />
                  </div>

                  {stage.hint && (
                    <div className="stage-hint-section">
                      <button
                        onClick={() => setShowHint(!showHint)}
                        className="stage-hint-button"
                      >
                        {showHint ? '🔼 Hide Hint' : '💡 Show Hint'}
                      </button>
                      {showHint && (
                        <p className="stage-hint-text">{stage.hint}</p>
                      )}
                    </div>
                  )}
                </div>
              )}

              {isFuture && (
                <div className="stage-future-content">
                  <div className="stage-locked">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                    <span>Complete previous steps first</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="stage-progress-info">
        Stage {currentStage + 1} of {stages.length}
      </div>

      <button
        onClick={handleSubmit}
        disabled={!answer.trim() || disabled}
        className="question-submit-button"
      >
        Submit Step
      </button>
    </div>
  );
}

export default StepByStep;
