



const modal = document.getElementById("popupModal");
// const openModalButton = document.getElementById("openModal");
const closeButton = document.querySelector(".close-button");
const cancelButton = document.getElementById("cancelButton");

// Open the modal
// openModalButton.onclick = function() {
//     modal.style.display = "block";
// }

// Close the modal when the close button is clicked
closeButton.onclick = function() {
    modal.style.display = "none";
}

// Close the modal when the cancel button is clicked
cancelButton.onclick = function() {
    modal.style.display = "none";
}

// Close the modal when clicking outside of the modal content
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
