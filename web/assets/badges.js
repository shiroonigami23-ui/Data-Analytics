document.addEventListener("DOMContentLoaded", () => {
  const badges = JSON.parse(localStorage.getItem("badges")) || {};
  const progress = JSON.parse(localStorage.getItem("progress")) || { topics: 0, quizzes: 0 };

  function unlockBadge(name, desc) {
    if (!badges[name]) {
      badges[name] = desc;
      localStorage.setItem("badges", JSON.stringify(badges));
      alert(`🎉 New Badge Unlocked: ${name} – ${desc}`);
      renderBadges();
    }
  }

  function updateProgress(type) {
    progress[type] = (progress[type] || 0) + 1;
    localStorage.setItem("progress", JSON.stringify(progress));

    if (type === "topics" && progress[type] >= 1) unlockBadge("First Reader", "Opened your first resource!");
    if (type === "quizzes" && progress[type] >= 1) unlockBadge("Quiz Starter", "Completed your first quiz!");
    if (type === "topics" && progress[type] >= 3) unlockBadge("Data Enthusiast", "Completed 3 topics!");
    if (type === "quizzes" && progress[type] >= 5) unlockBadge("Quiz Master", "Completed 5 quizzes!");
  }

  function renderBadges() {
    const badgeDiv = document.getElementById("badges");
    if (!badgeDiv) return;
    badgeDiv.innerHTML = "";
    Object.entries(badges).forEach(([name, desc]) => {
      const badge = document.createElement("div");
      badge.className = "badge";
      badge.innerHTML = `<strong>🏅 ${name}</strong><br><small>${desc}</small>`;
      badgeDiv.appendChild(badge);
    });
  }

  renderBadges();

  // Expose to global
  window.updateProgress = updateProgress;
});
