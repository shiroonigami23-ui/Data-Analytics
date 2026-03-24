document.addEventListener('DOMContentLoaded', () => {
    console.log("Website scripts loaded.");

    // --- Quiz Logic ---
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            // We fetch the answers from the JSON file to check correctness
            fetch('quiz.json')
                .then(res => res.json())
                .then(quizzes => {
                    let score = 0;
                    quizzes.forEach((q, idx) => {
                        const selected = document.querySelector(`input[name="q${idx}"]:checked`);
                        if (selected && selected.value === q.a) {
                            score++;
                        }
                    });
                    const resultDiv = document.getElementById('quiz-result');
                    resultDiv.innerHTML = `<h3>You scored ${score}/${quizzes.length}</h3>`;
                    if (score > 0 && window.updateProgress) {
                        window.updateProgress('quizzes');
                    }
                });
        });
    }

    // --- Translator/Dictionary Logic ---
    const popup = document.getElementById('dictionary-popup');
    const popupContent = document.getElementById('dictionary-content');

    if (popup) {
        document.addEventListener('mouseup', (event) => {
            const selectedText = window.getSelection().toString().trim();
            if (selectedText.length > 2 && !selectedText.includes(' ')) {
                popup.style.left = `${event.clientX}px`;
                popup.style.top = `${event.clientY + 15}px`;
                popup.style.display = 'block';
                fetchDefinition(selectedText);
            } else {
                popup.style.display = 'none';
            }
        });

        document.addEventListener('mousedown', (event) => {
            if (popup.style.display === 'block' && !popup.contains(event.target)) {
                popup.style.display = 'none';
            }
        });
    }

    async function fetchDefinition(word) {
        popupContent.innerHTML = `<em>Loading...</em>`;
        try {
            const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
            if (!response.ok) throw new Error('No definition found.');
            const data = await response.json();
            const firstMeaning = data[0]?.meanings[0]?.definitions[0];
            popupContent.innerHTML = `<strong>${data[0].word}</strong> (${data[0].meanings[0].partOfSpeech})<br>${firstMeaning.definition}`;
        } catch (error) {
            popupContent.innerHTML = `<strong>${word}</strong><br>No definition found.`;
        }
    }
});
