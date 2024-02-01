function showPassword() {
    var password_input = document.getElementById("password_input");
    if (password_input.type === "password") {
        password_input.type = "text";
    } else {
        password_input.type = "password";
    }
 }