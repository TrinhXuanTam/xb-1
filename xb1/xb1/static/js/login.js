var modal = document.getElementById("myModal");

var span = document.getElementsByClassName("close")[0];

var wrapper = document.getElementById("wrapper");

span.onclick = function() {
  modal.style.display = "none";
  wrapper.style.filter = "blur(0)"
};

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
    wrapper.style.filter = "blur(0)"
  }
};

function openDialog() {
  modal.style.display = "block";
  wrapper.style.filter = "blur(5px)"
}
