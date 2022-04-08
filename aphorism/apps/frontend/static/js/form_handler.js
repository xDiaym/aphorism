let button = document.querySelector(".submit");
function errorSetter(msg) {
    let parent = document.querySelector(".input_wrapper");
    let errorText = document.createElement("p");
    errorText.textContent = msg;
    parent.appendChild(errorText);
    setTimeout(() => {
        parent.removeChild(errorText);
    }, 5000);
}

button.addEventListener("click", () => {
    let firstPassword = document.querySelector("#password").value;
    let secondPassword = document.querySelector("#repeated_password").value;
    if (firstPassword !== secondPassword) {
        errorSetter("Passwords don't match");
    }
});
