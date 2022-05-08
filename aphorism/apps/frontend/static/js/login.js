import {login, redirectToMyFeed} from "./actions.js";


const email = document.querySelector("#email");
const password = document.querySelector("#password");
const button = document.querySelector(".submit");

button.addEventListener('click', () => {
  login(email.value, password.value)
    .then(redirectToMyFeed)
    .catch(alert) // TODO: display message
});
