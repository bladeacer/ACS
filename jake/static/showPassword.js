function showPassword() {
    var password_input = document.getElementById("password_input");
    if (password_input.type === "password") {
        password_input.type = "text";
    } else {
        password_input.type = "password";
    }
    var password_input = document.getElementById("password_input_new");
    if (password_input.type === "password") {
        password_input.type = "text";
    } else {
        password_input.type = "password";
    }
 }