/**
 * Mobile menu — only runs on small screens.
 * Toggles the class "is-open" on the nav link list.
 */
const menuButton = document.querySelector(".menu-button");
const navLinks = document.querySelector(".nav-links");

if (menuButton && navLinks) {
  menuButton.addEventListener("click", () => {
    menuButton.classList.toggle("is-open");
    navLinks.classList.toggle("is-open");
  });
}
