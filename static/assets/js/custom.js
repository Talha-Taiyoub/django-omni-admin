var modal = document.querySelector(".cmodal");
var trigger = document.querySelector(".trigger");
var closeButton = document.querySelector(".close-button");

function toggleModal() {
    modal.classList.toggle("show-modal");
}

function windowOnClick(event) {
    if (event.target === modal) {
        toggleModal();
    }
}

trigger.addEventListener("click", toggleModal);
closeButton.addEventListener("click", toggleModal);
window.addEventListener("click", windowOnClick);


function showPassword() {
    if (document.querySelector("#password").type === "password") {
      document.querySelector("#password").type = "text";
    } else {
      document.querySelector("#password").type = "password";
    }
    document.querySelector("#showPassword").classList.toggle("hidden");
    document.querySelector("#hidePassword").classList.toggle("hidden");
  }