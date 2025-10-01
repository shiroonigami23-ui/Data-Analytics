document.addEventListener("DOMContentLoaded", () => {
  // Quiz generator (simple example)
  const quizBtn = document.getElementById("generateQuiz");
  if (quizBtn) {
    quizBtn.addEventListener("click", () => {
      const container = document.getElementById("quizContainer");
      container.innerHTML = "<p>Q: Regression is used for...?<br>A) Grouping data<br>B) Predicting values<br>C) Visualization</p>";
    });
  }

  // Resource search (demo only)
  const searchBar = document.getElementById("searchBar");
  if (searchBar) {
    searchBar.addEventListener("input", (e) => {
      const filter = e.target.value.toLowerCase();
      document.querySelectorAll("#resourceList li").forEach(li => {
        li.style.display = li.textContent.toLowerCase().includes(filter) ? "" : "none";
      });
    });
  }
});
