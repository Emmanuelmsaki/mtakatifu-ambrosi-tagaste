document.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", function () {
      // Remove 'active' from all links
      document
        .querySelectorAll(".nav-link")
        .forEach((link) => link.classList.remove("active"));
      // Add 'active' to the clicked link
      this.classList.add("active");
    });
  });