// ============================================================
// WellVia - Frontend JavaScript
// ============================================================
// This file handles:
//  1. Mobile navigation toggle
//  2. Highlighting the active nav link
//  3. Smooth form validation feedback
//  4. Character counter for description textarea
// ============================================================


// ---- 1. Mobile Navigation Toggle ----
document.addEventListener("DOMContentLoaded", function () {

  const toggle = document.getElementById("nav-toggle");
  const navLinks = document.getElementById("nav-links");

  if (toggle && navLinks) {
    toggle.addEventListener("click", function () {
      // Add or remove the "open" class to show/hide the menu
      navLinks.classList.toggle("open");
    });

    // Close menu when a link is clicked (on mobile)
    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("open");
      });
    });
  }


  // ---- 2. Highlight the active navigation link ----
  // Compare the current page URL with each nav link's href
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-links a").forEach(function (link) {
    const linkPath = new URL(link.href, window.location.origin).pathname;
    if (linkPath === currentPath) {
      link.classList.add("active");
    }
  });


  // ---- 3. Client-side form validation (gentle feedback) ----
  // Adds a red border to empty required fields before submitting
  const forms = document.querySelectorAll("form[data-validate]");

  forms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      let hasError = false;

      // Check every field that has the "required" attribute
      form.querySelectorAll("[required]").forEach(function (field) {
        if (!field.value.trim()) {
          field.style.borderColor = "#dc2626"; // Red border
          hasError = true;
        } else {
          field.style.borderColor = ""; // Reset to default
        }
      });

      if (hasError) {
        e.preventDefault(); // Stop form submission
        // Scroll to the first red field
        const firstError = form.querySelector("[required]");
        if (firstError) firstError.focus();
      }
    });

    // Remove red border as soon as the user starts typing
    form.querySelectorAll("[required]").forEach(function (field) {
      field.addEventListener("input", function () {
        field.style.borderColor = "";
      });
    });
  });


  // ---- 4. Character counter for description textarea ----
  const descTextarea = document.getElementById("description");
  const charCounter = document.getElementById("char-count");

  if (descTextarea && charCounter) {
    descTextarea.addEventListener("input", function () {
      const remaining = 500 - descTextarea.value.length;
      charCounter.textContent = remaining + " characters remaining";

      // Warn when getting close to the limit
      charCounter.style.color = remaining < 50 ? "#dc2626" : "#94a3b8";
    });
  }


  // ---- 5. Auto-dismiss success alerts after 5 seconds ----
  const successAlert = document.querySelector(".alert-success.auto-dismiss");
  if (successAlert) {
    setTimeout(function () {
      successAlert.style.transition = "opacity 0.5s";
      successAlert.style.opacity = "0";
      setTimeout(function () { successAlert.remove(); }, 500);
    }, 5000);
  }

});
