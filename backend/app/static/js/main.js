document.addEventListener("DOMContentLoaded", () => {
  const flash = document.getElementById("flash-messages");
  if (flash && flash.dataset.message) {
    flash.innerHTML = `<div class="alert alert-info">${flash.dataset.message}</div>`;
  }

  const logoutLink = document.getElementById("logout-link");
  if (logoutLink) {
    logoutLink.addEventListener("click", (e) => {
      e.preventDefault();
      localStorage.removeItem("access_token");
      window.location.href = "/login";
    });
  }
});
