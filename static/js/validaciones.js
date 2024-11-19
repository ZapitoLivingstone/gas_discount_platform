// validaciones.js

// Función para validar el formulario
function validarFormulario(event) {
  event.preventDefault();  // Prevenir el envío del formulario

  // Obtener los valores de los campos
  const email = document.getElementById("email").value;
  const nuevaContraseña = document.getElementById("nueva_contraseña").value;
  const confirmarContraseña = document.getElementById("confirmar_contraseña").value;

  let errores = []; // Arreglo para almacenar los errores

  // Validación de email
  if (!email) {
    errores.push("El campo de correo electrónico es obligatorio.");
  }

  // Validación de contraseñas
  if (!nuevaContraseña) {
    errores.push("El campo de nueva contraseña es obligatorio.");
  } else if (nuevaContraseña !== confirmarContraseña) {
    errores.push("Las contraseñas no coinciden.");
  }

  // Mostrar errores o enviar formulario
  if (errores.length > 0) {
    mostrarErrores(errores);  // Mostrar los errores en la página
  } else {
    // Si no hay errores, enviar el formulario
    document.getElementById("formulario-cambiar").submit();  // Enviar el formulario
  }
}

// Función para mostrar los errores en la página
function mostrarErrores(errores) {
  // Obtener el contenedor de errores
  const contenedorErrores = document.getElementById("errores");
  
  // Limpiar los errores anteriores
  contenedorErrores.innerHTML = '';

  // Mostrar los nuevos errores
  errores.forEach(function(error) {
    const errorElement = document.createElement("div");
    errorElement.classList.add("alert", "alert-danger");
    errorElement.textContent = error;
    contenedorErrores.appendChild(errorElement);
  });
}

// Asociar la función de validación al formulario
document.addEventListener("DOMContentLoaded", function() {
  const formulario = document.getElementById("formulario");
  formulario.addEventListener("submit", validarFormulario);
});
