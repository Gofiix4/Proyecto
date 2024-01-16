document.addEventListener("DOMContentLoaded", function() {
    const signin_form = document.getElementById("signin_form");
    const iniciar = document.getElementById("iniciar");
  
    signin_form.addEventListener("submit", function(event) {
      // Validar que los campos estén llenos
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      // Puedes agregar más campos y validaciones según tus necesidades.
  
      if (username === "" || password === "") {
        alert("Por favor, llene todos los campos");
        event.preventDefault(); // Evita que el formulario se envíe
      }
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const signup_form = document.getElementById("signup_form");
    const registrar = document.getElementById("registrar");
  
    signup_form.addEventListener("submit", function(event) {
      // Validar que los campos estén llenos
      const first_name = document.getElementById("first_name").value;
      const last_name = document.getElementById("last_name").value;
      const email = document.getElementById("email").value;
      const username = document.getElementById("username").value;
      // Puedes agregar más campos y validaciones según tus necesidades.
  
      if (first_name === "" || last_name === "" || email === "" || username === "") {
        alert("Por favor, llene todos los campos");
        event.preventDefault(); // Evita que el formulario se envíe
      }
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const update_form = document.getElementById("update_form");
    const actualizar = document.getElementById("actualizar");
  
    update_form.addEventListener("submit", function(event) {
      // Validar que los campos estén llenos
      const first_name = document.getElementById("first_name").value;
      const last_name = document.getElementById("last_name").value;
      const email = document.getElementById("email").value;
      const username = document.getElementById("username").value;
      // Puedes agregar más campos y validaciones según tus necesidades.
  
      if (first_name === "" || last_name === "" || email === "" || username === "") {
        alert("Por favor, llene todos los campos");
        event.preventDefault(); // Evita que el formulario se envíe
      }
      else{
        var respuesta = window.confirm("¿Realmente deseas actualizar los datos de tu perfil?");

        if (respuesta) {
        } else {
          event.preventDefault();
        }

      }
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const updatePwd_form = document.getElementById("updatePwd_form");
    const actualizarPwd = document.getElementById("actualizarPwd");
  
    updatePwd_form.addEventListener("submit", function(event) {
      // Validar que los campos estén llenos
      const currentPassword = document.getElementById("currentPassword").value;
      const newPassword = document.getElementById("newPassword").value;
      const confirmPassword = document.getElementById("confirmPassword").value;
      // Puedes agregar más campos y validaciones según tus necesidades.
  
      if (currentPassword === "" || newPassword === "" || confirmPassword === "") {
        alert("Por favor, llene todos los campos");
        event.preventDefault(); // Evita que el formulario se envíe
      } else{
        if (newPassword == confirmPassword) {
          var respuesta = window.confirm("¿Realmente deseas actualizar tu contraseña?");
          if (respuesta) {
            alert("ba");
          } else {
            event.preventDefault();
          }
        } else{
          alert("Las contraseñas no coinciden");
          event.preventDefault(); // Evita que el formulario se envíe
        }

      }
    });
  });
  