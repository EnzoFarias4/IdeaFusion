import { fetchIdeas, createIdea, updateIdea, deleteIdea } from './api.js';

document.addEventListener('DOMContentLoaded', init);

function init() {
  displayIdeas();
  document.getElementById('createIdeaForm').addEventListener('submit', handleCreateIdea);
  document.addEventListener('click', handleActionClick);
}

async function displayIdeas() {
  try {
    const ideas = await fetchIdeas();
    const ideasList = document.getElementById('ideasList');
    let ideasHTML = '';
    ideas.forEach(idea => {
      ideasHTML += `<li>${idea.title} - ${idea.description}
                    <button class="edit-idea-btn" data-id="${idea.id}">Edit</button>
                    <button class="delete-idea-btn" data-id="${idea.id}">Delete</button></li>`;
    });
    ideasList.innerHTML = ideasHTML;
  } catch (error) {
    console.error('Failed to fetch ideas:', error);
  }
}

async function handleCreateIdea(event) {
  event.preventDefault();
  const title = event.target.title.value;
  const description = event.target.description.value;
  try {
    await createIdea({ title, description });
    event.target.reset();
    displayIdeas();
  } catch (error) {
    console.error('Failed to create an idea:', error);
  }
}

async function handleActionClick(event) {
  if (event.target.matches('.edit-idea-btn')) {
    handleEditIdea(event);
  } else if (event.target.matches('.delete-idea-btn')) {
    handleDeleteIdea(event);
  }
}

async function handleEditIdea(event) {
  const id = event.target.dataset.id;
  const title = prompt('Enter the new title:');
  const description = prompt('Enter the new description:');
  if (title && description) { // Only proceed if title and description are provided
    try {
      await updateIdea(id, { title, description });
      displayIdeas();
    } catch (error) {
      console.error('Failed to update idea:', error);
    }
  }
}

async function handleDeleteIdea(event) {
  const id = event.target.dataset.id;
  if (confirm('Are you sure you want to delete this idea?')) { // Add confirmation before deleting
    try {
      await deleteIdea(id);
      displayIdeas();
    } catch (error) {
      console.error('Failed to delete idea:', error);
    }
  }
}