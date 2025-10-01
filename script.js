document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('feedback-form');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const response = await fetch('https://script.google.com/macros/s/AKfycbxuFHf4WlRXYq2I0QJdC5D3zolFzg70moOFoKJIwDklQRfugmD8LYsl4JZ3Z9hTIonhKw/exec', {
        method: 'POST',
        body: data
      });
      document.getElementById('feedback-response').innerText = 'Thank you for your feedback!';
      form.reset();
    });
  }
});