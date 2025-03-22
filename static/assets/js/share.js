
document.addEventListener("DOMContentLoaded", function () {
  const pageUrl = encodeURIComponent(window.location.href); // Get current page URL
  const pageTitle = encodeURIComponent(document.title); // Get page title

    // Email sharing
    document.getElementById("email-share").href =
    `mailto:?subject=${pageTitle}&body=Soma Makala hii: ${pageTitle} ${pageUrl}`;

  // X (Twitter) sharing
  document.getElementById("x-share").href =
    `https://twitter.com/intent/tweet?url=${pageUrl}&text=${pageTitle}`;

  // WhatsApp sharing
  document.getElementById("whatsapp-share").href =
    `https://api.whatsapp.com/send?text=${pageTitle} ${pageUrl}`;

});
