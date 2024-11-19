document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
  
    form.addEventListener('submit', function (event) {
        let hasError = false;
  
        // Validar email
        if (!emailInput.value.trim()) {
            emailInput.classList.add('is-invalid');
            hasError = true;
        } else if (!/\S+@\S+\.\S+/.test(emailInput.value.trim())) {
            emailInput.classList.add('is-invalid');
            hasError = true;
        } else {
            emailInput.classList.remove('is-invalid');
        }
  
        // Validar password
        if (!passwordInput.value.trim()) {
            passwordInput.classList.add('is-invalid');
            hasError = true;
        } else {
            passwordInput.classList.remove('is-invalid');
        }
  
        // Evitar envío si hay errores
        if (hasError) {
            event.preventDefault();
        }
    });
  });
  