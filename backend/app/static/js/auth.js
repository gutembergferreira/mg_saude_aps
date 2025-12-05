document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("login-form");
  const alertBox = document.getElementById("login-alert");

  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (alertBox) {
      alertBox.classList.add("d-none");
      alertBox.textContent = "";
    }

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const resp = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, senha: password }),
      });

      if (!resp.ok) {
        throw new Error("Credenciais inválidas");
      }

      const data = await resp.json();
      const token = data.access_token;
      if (token) {
        localStorage.setItem("access_token", token);
        window.location.href = "/dashboard";
      } else {
        throw new Error("Token não retornado");
      }
    } catch (err) {
      if (alertBox) {
        alertBox.textContent = err.message || "Erro ao autenticar";
        alertBox.classList.remove("d-none");
      } else {
        alert(err.message);
      }
    }
  });
});
