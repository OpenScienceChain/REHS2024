const mobile = document.querySelector(".menu_button");
const navMenu = document.querySelector(".menu");

mobile.addEventListener("click", mobileMenu);

function mobileMenu() {
    mobile.classList.toggle("active");
    navMenu.classList.toggle("active");
}