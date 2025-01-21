import { getStorage, ref, uploadBytesResumable, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-storage.js";

// Function to generate a unique file name
function generateFileName() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day}_${hours}-${minutes}-${seconds}`;
}

const storage = getStorage();
const storageRef = ref(storage, generateFileName());

// Assuming you have a file input element with ID 'fileInput' in your HTML
const fileInput = document.getElementById('fileInput');

// Listen for changes in the file input
fileInput.addEventListener('change', handleFileSelect);
document.getElementById('fileInput').addEventListener("change", function () {
    startCountdown();
    displayLoading();
    blurBackground();
});
function displayLoading() {
    const disp = document.getElementById('loading-container');
    disp.style.display = "block";
}
function blurBackground() {
    const main = document.getElementById('main');
    main.style.filter = "blur(8px)";
}

function updateProgressBar(progress) {
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = progress + '%';
}

function handleFileSelect(event) {
    const file = event.target.files[0]; // Get the first file selected by the user

    // Create a Blob object from the selected file
    const blob = new Blob([file]);

    // Adjust the content type based on the actual file format
    const contentType = file.type;

    // Upload the Blob to Firebase Storage
    displayLoading();
    blurBackground();
    const uploadTask = uploadBytesResumable(storageRef, blob, { contentType });
    uploadTask.on('state_changed',
        (snapshot) => {
            // Handle progress, pause, and resume states
            if (snapshot && typeof snapshot.bytesTransferred !== 'undefined' && typeof snapshot.totalBytes !== 'undefined') {
                const progress = Math.floor((snapshot.bytesTransferred / snapshot.totalBytes) * 100);
                updateProgressBar(progress);
                document.getElementById("upload-progress").textContent = progress + "%";
            } else {
                console.error("Snapshot or its properties are undefined.");
            }
            console.log('Upload is ' + progress + '% done');
            switch (snapshot.state) {
                case 'paused':
                    console.log('Upload is paused');
                    break;
                case 'running':
                    console.log('Upload is running');
                    break;
            }
        },
        (error) => {
            console.error('Upload error:', error);
        },
        () => {
            // Handle successful uploads on complete
            getDownloadURL(uploadTask.snapshot.ref).then((downloadURL) => {
                window.location.href = "result.html";
            });
        }
    );
}

