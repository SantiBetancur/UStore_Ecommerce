document.addEventListener("DOMContentLoaded", () => {
    console.log("checkPassword.js loaded ✅");

    // Busca el formulario (ajusta el id si usas otro)
    const form = document.getElementById("signin-form");

    if (form) {
        form.addEventListener("submit", (event) => {
            if (!validatePassword()) {
                event.preventDefault(); // ❌ Detiene el envío si no pasa validación
            }
        });
    }
});

function validatePassword() {
    const password = document.getElementById("password").value;
    const errorSpan = document.getElementById("password-error");

    const minLength = /.{8,}/;
    const upperCase = /[A-Z]/;
    const lowerCase = /[a-z]/;
    const number = /\d/;
    const specialChar = /[@$!%*?&]/;

    if (!minLength.test(password)) {
        errorSpan.textContent = "La contraseña debe tener al menos 8 caracteres.";
        return false;
    }
    if (!upperCase.test(password)) {
        errorSpan.textContent = "Debe contener al menos una mayúscula.";
        return false;
    }
    if (!lowerCase.test(password)) {
        errorSpan.textContent = "Debe contener al menos una minúscula.";
        return false;
    }
    if (!number.test(password)) {
        errorSpan.textContent = "Debe contener al menos un número.";
        return false;
    }
    if (!specialChar.test(password)) {
        errorSpan.textContent = "Debe contener al menos un carácter especial (@$!%*?&).";
        return false;
    }

    errorSpan.textContent = ""; // ✅ limpia el error
    return true; // deja que el form se envíe al backend
}
