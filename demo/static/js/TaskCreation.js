console.log("taskcreation.js loaded");

// DO NOTHING special — let the form submit normally
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[action='/add_task']");

    if (!form) return;

    form.addEventListener("submit", () => {
        console.log("Form submitted to backend");
        // no preventDefault
        // no localStorage
        // backend handles everything
    });
});