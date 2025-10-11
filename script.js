document.addEventListener('DOMContentLoaded', () => {
  console.log('Data Analytics Hub script loaded. Translator active. 🎉');

  const popup = document.getElementById('dictionary-popup');
  const popupContent = document.getElementById('dictionary-content');

  // Don't do anything if the popup element doesn't exist on the page
  if (!popup) {
    return;
  }

  // Listen for when the user releases the mouse button
  document.addEventListener('mouseup', (event) => {
    // Get the text the user has highlighted
    const selectedText = window.getSelection().toString().trim();

    // If the selected text is a single, valid word...
    if (selectedText.length > 2 && !selectedText.includes(' ')) {
      
      // Position the popup near the selected text
      popup.style.left = `${event.clientX}px`;
      popup.style.top = `${event.clientY + 15}px`; // Show it just below the cursor
      
      // Show the popup and fetch the definition
      popup.style.display = 'block';
      fetchDefinition(selectedText);

    } else {
      // If no valid word is selected, hide the popup
      popup.style.display = 'none';
    }
  });

  // Hide the popup if the user clicks anywhere else on the page
  document.addEventListener('mousedown', (event) => {
    // Check if the click was outside the popup
    if (popup.style.display === 'block' && !popup.contains(event.target)) {
      popup.style.display = 'none';
    }
  });

  // --- Dictionary API Fetch Function ---
  async function fetchDefinition(word) {
    popupContent.innerHTML = `<em>Loading definition for <strong>${word}</strong>...</em>`;

    try {
      // We use a free, public dictionary API for this
      const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
      
      if (!response.ok) {
        popupContent.innerHTML = `<strong>${word}</strong><br>Sorry, no definition found.`;
        return;
      }

      const data = await response.json();
      const firstMeaning = data[0]?.meanings[0]?.definitions[0];

      if (firstMeaning) {
        popupContent.innerHTML = `<strong>${data[0].word}</strong> (${data[0].meanings[0].partOfSpeech})<br>${firstMeaning.definition}`;
      } else {
        popupContent.innerHTML = `<strong>${word}</strong><br>Sorry, no definition found.`;
      }

    } catch (error) {
      console.error("Dictionary API error:", error);
      popupContent.innerHTML = `<strong>${word}</strong><br>Could not fetch definition.`;
    }
  }
});
