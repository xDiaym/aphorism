import {redirectToMyFeed, register} from "./actions.js"

const errorArea = document.querySelector(".input_wrapper");

/** @param {String} message - error message*/
function setError(message) {
  const errorText = document.createElement("p");
  errorText.textContent = message;
  // FIXME: many toasts
  errorArea.appendChild(errorText);
  setTimeout(() => {
    errorArea.removeChild(errorText);
  }, 5000);
}


const password = document.querySelector("#password");
const repeatedPassword = document.querySelector("#repeated_password");
const button = document.querySelector(".submit");
const email = document.querySelector('#email');
const slug = document.querySelector('#nickname');
const name = document.querySelector('#display_name');
button.addEventListener("click", async () => {
  if (password.value === repeatedPassword.value) {
    register(email.value, password.value, slug.value, name.value)
      .then(redirectToMyFeed)
      .catch(e => setError(e.message))
  } else {
    setError("Passwords don't match");
  }
});
