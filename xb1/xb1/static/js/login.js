var modal = document.getElementById("login_modal");

var span = document.getElementsByClassName("close")[0];

var wrapper = document.getElementById("wrapper");

span.onclick = function() {
  wrapper.style.filter = "blur(0)";
  modal.style.transition = "1s";
  modal.style.opacity = 0;
  modal.style.visibility = "hidden";
};

wrapper.onclick = function(event) {
  if (event.target == modal) {
    wrapper.style.filter = "blur(0)";
    modal.style.transition = "1s";
    modal.style.opacity = 0;
    modal.style.visibility = "hidden";
  }
};

function openDialog() {
  modal.style.transition = "3s";
  modal.style.visibility = "visible";
  modal.style.opacity = 1;
  wrapper.style.filter = "blur(10px)";
}