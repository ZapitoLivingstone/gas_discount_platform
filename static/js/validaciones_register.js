document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const nombreInput = document.getElementById('nombre');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
  
    // Validación del formulario
    form.addEventListener('submit', function (e) {
      let hasErrors = false;
      let errorMessage = '';
  
      if (!nombreInput.value) {
        hasErrors = true;
        nombreInput.classList.add('is-invalid');
      } else {
        nombreInput.classList.remove('is-invalid');
      }
  
      if (!emailInput.value || !emailInput.validity.valid) {
        hasErrors = true;
        emailInput.classList.add('is-invalid');
      } else {
        emailInput.classList.remove('is-invalid');
      }
  
      if (!passwordInput.value) {
        hasErrors = true;
        passwordInput.classList.add('is-invalid');
      } else {
        passwordInput.classList.remove('is-invalid');
      }
  
      if (passwordInput.value !== confirmPasswordInput.value) {
        hasErrors = true;
        confirmPasswordInput.classList.add('is-invalid');
      } else {
        confirmPasswordInput.classList.remove('is-invalid');
      }
  
      if (hasErrors) {
        e.preventDefault();
      }
    });
  });
  