const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");

dropArea.addEventListener("click", () => fileInput.click());

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.borderColor = "#22c55e";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.borderColor = "#334155";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
});