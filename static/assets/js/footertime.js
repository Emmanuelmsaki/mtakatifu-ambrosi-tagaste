 // Create a Date object for Tanzania's timezone (EAT is UTC+3)
 const tanzaniaTime = new Date().toLocaleString("en-US", {
    timeZone: "Africa/Dar_es_Salaam",
  });

  // Get the year from the localized date
  const currentYear = new Date(tanzaniaTime).getFullYear();

  // Insert the year into the element
  document.getElementById("currentYear").textContent = currentYear;