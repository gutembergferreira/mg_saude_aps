document.addEventListener("DOMContentLoaded", () => {
  const flash = document.getElementById("flash-messages");
  if (flash && flash.dataset.message) {
    flash.innerHTML = `<div class="alert alert-info">${flash.dataset.message}</div>`;
  }
});
