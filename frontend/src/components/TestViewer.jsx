export default function TestViewer({ testData }) {
  if (!testData) return null;

  if (testData.guardrail && !testData.guardrail.is_topic_relevant) {
    return (
      <div className="test-viewer error-box">
        <h3>Topic Rejected</h3>
        <p>{testData.guardrail.rejection_reason}</p>
      </div>
    );
  }

  return (
    <div className="test-viewer">
      <h2>Mock Test: {testData.topic}</h2>
      
      {testData.mcq_questions?.length > 0 && (
        <div>
          <h3>Multiple Choice Questions</h3>
          {testData.mcq_questions.map((q, idx) => (
            <div key={idx} className="question-card">
              <p><strong>Q{idx + 1}:</strong> {q.question}</p>
              <ul>
                {q.options.map((opt, i) => (
                  <li key={i}>{opt}</li>
                ))}
              </ul>
              <details>
                <summary>Show Answer</summary>
                <p><strong>Answer:</strong> {q.correct_answer}</p>
                <p><em>{q.explanation}</em></p>
              </details>
            </div>
          ))}
        </div>
      )}

      {testData.subjective_questions?.length > 0 && (
        <div style={{ marginTop: '32px' }}>
          <h3>Subjective Questions</h3>
          {testData.subjective_questions.map((q, idx) => (
            <div key={idx} className="question-card">
              <p><strong>Q{idx + 1}:</strong> {q.question}</p>
              <details>
                <summary>Show Rubric & Ideal Answer</summary>
                <p><strong>Grading Rubric:</strong> {q.grading_rubric}</p>
                <p><strong>Ideal Answer:</strong> {q.example_ideal_answer}</p>
              </details>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
