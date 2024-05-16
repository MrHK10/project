const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');

  loginForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission
      // You can perform additional client-side validation here if needed
      loginForm.submit(); // Trigger the form submission
  });

  signupForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent the default form submission
      // You can perform additional client-side validation here if needed
      signupForm.submit(); // Trigger the form submission
  });
});
