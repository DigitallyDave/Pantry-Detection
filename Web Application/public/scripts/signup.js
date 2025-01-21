import { app } from "./firebase-config.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { ref, uploadBytes, getStorage, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-storage.js";

const auth = getAuth(app);

const signUpForm = document.getElementById("signup-form");

signUpForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById("newEmail").value;
    const password = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const profilePicture = document.getElementById("profilePicture").files[0];
    if (password !== confirmPassword) {
        alert(newPassword + confirmPassword);
        alert("Passwords do not match");
        return;
    }

    createUserWithEmailAndPassword(auth,email,password)
        .then(async (userCredential) => {
            const user = userCredential.user;
            console.log("User signed-up: ", user);
            const storage = getStorage(app);
            console.log(user.uid);
            const storageRef = ref(storage,'profile_pictures/' + user.uid);
            await uploadBytes(storageRef, profilePicture);
            window.location.href = "index.html";
        })
        .catch((error) => {
            console.log(error);
            alert(error);
        });
});