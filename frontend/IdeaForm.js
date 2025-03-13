import React, { useState, useCallback } from 'react';

const IdeaForm = ({ onSubmit, initialData = {} }) => {
  const [formData, setFormData] = useState({
    title: initialData.title || '',
    description: initialData.description || '',
  });
  const [error, setError] = useState('');

  const outputLog = useCallback((message) => {
    console.log(`[IdeaForm Log]: ${message}`);
  }, []);

  const isFormValid = useCallback(() => {
    const { title, description } = formData;
    if (!title || !description) {
      setError('Both title and description are required.');
      outputLog('Validation failed: Both title and description are required.');
      return false;
    }
    setError(''); // Clear previous errors
    return true;
  }, [formData, outputLog]);

  const handleFormChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    outputLog(`${name} changed: ${value}`);
  }, [outputLog]);

  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    outputLog('Submitting the form.');

    if (!isFormValid()) return;

    onSubmit(formData);
    outputLog('Form submitted successfully with data: ' + JSON.stringify(formData));
  }, [formData, isFormValid, onSubmit, outputLog]);

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error}</div>}
      <div className="form-group">
        <label htmlFor="title">Title</label>
        <input
          type="text"
          name="title"
          id="title"
          value={formData.title}
          onChange={handleFormChange}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          name="description"
          id="description"
          rows="5"
          value={formData.description}
          onChange={handleFormChange}
          required
        ></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default IdeaForm;