import React, { useState } from 'react';

const IdeaForm = ({ onSubmit, initialData }) => {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [error, setError] = useState('');

  const outputLog = (message) => {
    console.log(`[IdeaForm Log]: ${message}`);
  };

  const validateForm = () => {
    if (!title || !description) {
      setError('Both title and description are required.');
      outputLog('Validation failed: Both title and description are required.');
      return false;
    }
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    outputLog('Submitting the form.');

    if (!validateForm()) return;

    const ideaData = {
      title,
      description,
    };

    onSubmit(ideaData);
    outputLog('Form submitted successfully with data: ' + JSON.stringify(ideaData));
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      <div className="form-group">
        <label htmlFor="title">Title</label>
        <input
          type="text"
          name="title"
          id="title"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            outputLog(`Title changed: ${e.target.value}`);
          }}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          name="description"
          id="description"
          rows="5"
          value={description}
          onChange={(e) => {
            setDescription(e.target.value);
            outputLog(`Description changed: ${e.target.value}`);
          }}
          required
        ></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default IdeaForm;