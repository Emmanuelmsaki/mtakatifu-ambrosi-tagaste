document.addEventListener("DOMContentLoaded", function () {
    const dateElements = document.querySelectorAll(".current-date"); // Select all elements with class 'current-date'
    const currentDate = new Date().toLocaleDateString("sw-TZ", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });

    dateElements.forEach((element) => {
      element.textContent = currentDate; // Update each element's content
    });
  });