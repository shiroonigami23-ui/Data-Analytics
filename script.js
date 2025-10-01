document.addEventListener("DOMContentLoaded", () => {
  const searchBar = document.getElementById("searchBar");
  const resourceList = document.getElementById("resourceList");
  const noResults = document.getElementById("noResults");

  // ✅ Page Visit Tracker
  fetch("data/analytics.json")
    .then(response => response.json())
    .then(data => {
      const page = window.location.pathname.split("/").pop() || "index.html";
      data.visits[page] = (data.visits[page] || 0) + 1;

      // Save updated analytics locally (for offline dev)
      fetch("update.py", { method: "POST", body: JSON.stringify(data) }).catch(() => {});
    });

  // ✅ Search Functionality
  if (searchBar) {
    searchBar.addEventListener("keyup", () => {
      const filter = searchBar.value.toLowerCase();
      const items = resourceList.getElementsByTagName("li");
      let found = false;

      for (let i = 0; i < items.length; i++) {
        const text = items[i].innerText.toLowerCase();
        if (text.includes(filter)) {
          items[i].style.display = "";
          found = true;
        } else {
          items[i].style.display = "none";
        }
      }
      noResults.style.display = found ? "none" : "block";

      // Save search term
      if (filter.length > 2) {
        fetch("data/analytics.json")
          .then(res => res.json())
          .then(data => {
            data.searches.push(filter);
            fetch("update.py", { method: "POST", body: JSON.stringify(data) }).catch(() => {});
          });
      }
    });
  }
});